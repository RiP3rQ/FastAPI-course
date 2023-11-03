# ------------------------------------------------------------------ IMPORTS ------------------------------------------------------------------ #

from typing import  Optional
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, status, Response, Depends
from random import randint
import psycopg2
from psycopg2.extras import RealDictCursor
import time

from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db


# ------------------------------------------------------------------ APP ------------------------------------------------------------------ #

app = FastAPI()

models.Base.metadata.create_all(bind=engine)



# model for post
class Post(BaseModel):
    title: str
    content: str
    published: bool = False


#basic api route
@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post, db: Session = Depends(get_db)):
    # post = models.Post(title=post.title, content=post.content, published=post.published) --> this is the same as the line below but with less code
    post = models.Post(**post.model_dump())
    db.add(post)
    db.commit()
    db.refresh(post)

    return post

@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    return post

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    deleted_post = db.query(models.Post).filter(models.Post.id == id)

    if deleted_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    deleted_post.delete(synchronize_session=False)    
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(id: int, post: Post, db: Session = Depends(get_db)):
    updated_post = db.query(models.Post).filter(models.Post.id == id)

    if updated_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    updated_post.update(post.model_dump(), synchronize_session=False)
    db.commit()
    
    return updated_post.first()