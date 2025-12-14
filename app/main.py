from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
# from fastapi.params import Body
# from random import randrange
# # import psycopg2 
# from psycopg2.extras import RealDictCursor
# import time
from sqlalchemy.orm import Session
from fastapi import Depends
from.import models
from.database import engine, SessionLocal, get_db
from.schemas import *
from.routers import post, user, auth, vote

models.Base.metadata.create_all(bind=engine)

app = FastAPI()  # uvicorn app.main:app --reload

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router)
app.include_router(post.router)
app.include_router(user.router)
app.include_router(vote.router)

# testing roots
@app.get("/")
def root():
    return {"Message": "Well Hello this is Just a test or A testing root ( really nothing to se here) please dont hack this app :)"}



