# ------------------------------------------------------------------ IMPORTS ------------------------------------------------------------------ #

from fastapi import HTTPException, status, Response, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(
    tags=["Authentication"],
)

# ------------------------------------------------------------------ AUTH ------------------------------------------------------------------ #
@router.post("/login")
def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()

    # check if user exists
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    # check if password is correct (compare hashed password with plain text password)
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect credentials")

    # create JWT token

    # return token

    return {"token": "token"}