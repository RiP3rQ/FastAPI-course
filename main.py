from typing import  Optional
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from random import randint

app = FastAPI()

# title str, content str
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [
    {"id": 1,"title": "Hello", "content": "World"},
    {"id": 2,"title": "Fast", "content": "API"},
    {"id": 3,"title": "Python", "content": "Programming"},
]

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/posts")
def get_posts():
    return {"Data": my_posts}

@app.post("/posts", status_code=201)
def create_post(newPost: Post):
    print (newPost)
    post_dict = newPost.model_dump()
    post_dict["id"] = randint(0,1000000)
    my_posts.append(post_dict)
    return post_dict

@app.get("/posts/{id}")
def get_post(id: int):
    for post in my_posts:
        if post["id"] == id:
            return post
    
    raise HTTPException(status_code=404, detail="Post not found")

@app.delete("/posts/{id}")
def delete_post(id: int):
    for index, post in enumerate(my_posts):
        if post["id"] == id:
            my_posts.pop(index)
            return {"message": "Post deleted successfully"}
    
    raise HTTPException(status_code=404, detail="Post not found")

