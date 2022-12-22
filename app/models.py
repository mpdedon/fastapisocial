from email.policy import default
from enum import unique
from tkinter.tix import Tree
from xmlrpc.client import Boolean
from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import null, text
from sqlalchemy.sql.sqltypes import TIMESTAMP


class Post(Base):

    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='True', nullable=False)
    time_created = Column(TIMESTAMP(timezone=True), 
                          nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"),
                                          nullable=False,server_default='1')
    owner = relationship("User")

class User(Base):

    __tablename__= "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    time_created = Column(TIMESTAMP(timezone=True), 
                                    nullable=False, server_default=text('now()'))
    phone = Column(String, nullable=True)


class Vote(Base):

    __tablename__ = "votes"

    user_id = Column(Integer, ForeignKey(
                    "users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey(
                    "posty.id", ondelete="CASCADE"), primary_key=True)


