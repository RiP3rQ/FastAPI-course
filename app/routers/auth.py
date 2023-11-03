# ------------------------------------------------------------------ IMPORTS ------------------------------------------------------------------ #

from fastapi import HTTPException, status, Response, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from ..database import get_db

router = APIRouter(
    tags=["Authentication"],
)

# ------------------------------------------------------------------ AUTH ------------------------------------------------------------------ #
@router.post("/login")
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    # check if user exists
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    # check if password is correct (compare hashed password with plain text password)
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect credentials")

    # create JWT token
    access_token = oauth2.create_access_token(data={"user_id": user.id})

    # return token
    return {"access_token" : access_token, "token_type" : "bearer"}