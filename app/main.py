# ------------------------------------------------------------------ IMPORTS ------------------------------------------------------------------ #

from fastapi import FastAPI

from . import models
from .database import engine
from .routers import post, user

# ------------------------------------------------------------------ APP ------------------------------------------------------------------ #

app = FastAPI() #create FastAPI instance

models.Base.metadata.create_all(bind=engine) #create tables in db with ORM

#origins = ["*"] #list of origins that can access the API

app.include_router(post.router) #include post routers
app.include_router(user.router) #include user routers

#basic api route
@app.get("/")
def read_root():
    return {"Hello": "World"}
