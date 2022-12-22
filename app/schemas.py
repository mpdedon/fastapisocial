from importlib.resources import Package
from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):

    email: EmailStr
    password: str

class UserDisplay(BaseModel):

    id: int
    email: EmailStr
    time_created: datetime

    class Config:
        orm_mode = True

class UserLogin(BaseModel):

    email: EmailStr
    password: str

class PostBase(BaseModel):

    title: str
    content: str
    published: bool=True
    time_created: datetime = datetime.now()
    #rating: Optional[int]=None

    class Config:
        orm_mode = True

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):

    id: int
    time_created: datetime
    owner_id: int
    owner: UserDisplay

    class Config:
        orm_mode = True

class PostDisplay(BaseModel):

    Post: PostResponse
    votes: int

    class Config:
        orm_mode = True

class Token(BaseModel):

    access_token: str
    token_type: str 

class TokenData(BaseModel):

    id: Optional[str] = None 

class Vote(BaseModel):

    post_id: int
    dir: conint(le=1)
