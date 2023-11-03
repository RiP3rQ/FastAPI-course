from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") #hashing password

def hash(password: str):
    return pwd_context.hash(password)