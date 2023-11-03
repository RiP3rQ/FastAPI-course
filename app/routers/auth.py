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
@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    # check if user exists
    if user == None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not found")
    
    # check if password is correct (compare hashed password with plain text password)
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect credentials")

    # create JWT token
    access_token = oauth2.create_access_token(data={"email": user.email})

    return {"access_token": access_token, "token_type": "bearer"}