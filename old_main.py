from random import randrange
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
import datetime
import psycopg
from psycopg import connect, ClientCursor
import time

app = FastAPI()

class Post(BaseModel):

    title: str
    content: str
    published: bool=True
    time_created = datetime.datetime.now()
    rating: Optional[int]=None

while True:
    try:
        conn = psycopg.connect(host='localhost', 
                            dbname='fastAPI', 
                            user='postgres', 
                            password='director',
                            cursor_factory=ClientCursor)
        cursor = conn.cursor()
        print("Database Connection was Successful!")
        break

    except Exception as error:
        print("Database Connection Failed!")
        print("Error: ", error)
        time.sleep(5)


my_posts = [{'title': 'First Title', 'content': 'This is the first content.', 'id': 1,'published': True, 'rating': 5},
            {'title': 'Second Title', 'content': 'This is the second content.', 'id': 2, 'published': True, 'rating': 4},
            {'title': 'Third Title', 'content': 'This is the third content.', 'id': 3, 'published': True, 'rating': 3}]

@app.get('/')
async def root():
    return {"message": "Assalamu Alaikum"}

@app.get('/posts')
def get_posts():

    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}

@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 10000)
    my_posts.append(post_dict)
    return {"message": post_dict}

def find_post(id):
    for post in my_posts:
        if post['id'] == id:
            return post

def find_index(id: int):
    for index, post in enumerate(my_posts):
        if post['id'] == id:
            return index

@app.get('/posts/{id}')
def get_post(id: int):

    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with the ID: {id} is not found')
    return {"Post detail": post}

@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):

    index = find_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with the ID: {id} is not found')
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put('/posts/{id}')
def update_post(id: int, post: Post):

    index = find_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with the ID: {id} is not found')
    
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
        
    return {"data": post_dict}
