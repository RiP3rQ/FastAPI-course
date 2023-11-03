from typing import  Optional
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, status, Response
from random import randint
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

# model for post
class Post(BaseModel):
    title: str
    content: str
    published: bool = False

# temp database
# my_posts = [
#     {"id": 1,"title": "Hello", "content": "World", "rating": 5, "published": True},
#     {"id": 2,"title": "Fast", "content": "API", "rating": 4, "published": False},
#     {"id": 3,"title": "Python", "content": "Programming", "rating": 5, "published": True},
# ]

# connection to database
while True:
    try:
        conn = psycopg2.connect(
            host = "localhost",
            database = "fastapi",
            user = "postgres",
            password = "admin",
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        print("Connected to database")
        break
    except Exception as error:
        print("Unable to connect to database")
        print(error)
        time.sleep(5)

#basic api route
@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/posts")
def get_posts():
    # return my_posts
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    return posts

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s)", (post.title, post.content, post.published))
    conn.commit()
    return {"data": f"Post with title {post.title} is created successfully"}


@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("SELECT * FROM posts WHERE id = %s", (str(id)))
    post = cursor.fetchone()
    if post:
        return post
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("DELETE FROM posts WHERE id = %s returning *", (str(id)))
    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(id: int, post: Post):
    cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s returning *", (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    return updated_post