from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import Optional
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models, schemas, oauth2
from .. database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get('/', response_model=List[schemas.PostDisplay])
def get_posts(
              db: Session = Depends(get_db),
              current_user: int=Depends(oauth2.get_current_user),
              limit: int = 10, skip: int = 0, search: Optional[str] = ""):

    #posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id==models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return post

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(
                post: schemas.PostCreate, #
                db: Session=Depends(get_db), 
                current_user: int=Depends(oauth2.get_current_user)
):
    new_post = models.Post(owner_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@router.get('/{id}', response_model=schemas.PostDisplay)
def get_post(id: int, db: Session = Depends(get_db), 
             current_user: int=Depends(oauth2.get_current_user)
):

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id==models.Post.id, isouter=True).group_by(
        models.Post.id).filter(models.Post.id == id).first()
   
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with the ID: {id} is not found')
    return post

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
                id: int, db: Session = Depends(get_db), 
                current_user: int=Depends(oauth2.get_current_user)
):

    post = db.query(models.Post).filter(models.Post.id == id)

    post_to_delete = post.first()

    if post_to_delete == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with the ID: {id} is not found')

    if post_to_delete.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Not authorizd to perform requested action!')

    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put('/{id}', response_model=schemas.PostCreate)
def update_post(
                id: int, new_post: schemas.PostCreate, 
                db: Session = Depends(get_db), 
                current_user: int=Depends(oauth2.get_current_user)
):

    post_to_update = db.query(models.Post).filter(models.Post.id == id)

    post = post_to_update.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with the ID: {id} is not found')

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Not authorizd to perform requested action!')

    post_to_update.update(new_post.dict(), synchronize_session=False)
    db.commit()
    return post_to_update.first()

