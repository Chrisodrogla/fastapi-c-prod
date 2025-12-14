from fastapi import FastAPI, Response, status, HTTPException, APIRouter
from fastapi import Depends
from .. import models,schemas,utils
from sqlalchemy.orm import Session
from..database import engine, SessionLocal, get_db
from..schemas import *
from..routers import post, user


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


# CREATE USER 
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # hash the password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.model_dump())
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with email {user.email} already exists")
    db.add(new_user)
    db.commit() 
    db.refresh(new_user)
    return new_user

# GET USER
@router.get("/id/{id}", response_model=UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {id} was not found")
    return user
