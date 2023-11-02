from typing import  Optional
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, status, Response
from random import randint

app = FastAPI()

# title str, content str
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [
    {"id": 1,"title": "Hello", "content": "World", "rating": 5, "published": True},
    {"id": 2,"title": "Fast", "content": "API", "rating": 4, "published": False},
    {"id": 3,"title": "Python", "content": "Programming", "rating": 5, "published": True},
]

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/posts")
def get_posts():
    return {"Data": my_posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
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
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    for index, post in enumerate(my_posts):
        if post["id"] == id:
            my_posts.pop(index)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(id: int, post: Post):
    print (post)
    for index, item in enumerate(my_posts):
        if item["id"] == id:
            my_posts[index] = post
            return {"message": "Post updated successfully"}
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")