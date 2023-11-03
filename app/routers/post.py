# ------------------------------------------------------------------ IMPORTS ------------------------------------------------------------------ #

from fastapi import HTTPException, status, Response, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from typing import List


router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
)

# ------------------------------------------------------------------ POSTS ------------------------------------------------------------------ #
@router.get("/", response_model = List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model = schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # post = models.Post(title=post.title, content=post.content, published=post.published) --> this is the same as the line below but with less code
    post = models.Post(**post.model_dump())
    db.add(post)
    db.commit()
    db.refresh(post)

    return post

@router.get("/{id}", response_model = schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    deleted_post = db.query(models.Post).filter(models.Post.id == id)

    if deleted_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    deleted_post.delete(synchronize_session=False)    
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model = schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    updated_post = db.query(models.Post).filter(models.Post.id == id)

    if updated_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    updated_post.update(post.model_dump(), synchronize_session=False)
    db.commit()
    
    return updated_post.first()
