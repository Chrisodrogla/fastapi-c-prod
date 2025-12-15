from fastapi import FastAPI, Response, status, HTTPException, APIRouter
from fastapi import Depends
from sqlalchemy import func
from .. import models, schemas, utils, oauth2
from sqlalchemy.orm import Session
from..database import engine, SessionLocal, get_db
from..schemas import *

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

# GET ALL POSTS
# @router.get("/", response_model=list[Post]) 
# def get_posts(db: Session = Depends(get_db), current_user_id: int = Depends(oauth2.get_current_user), limit : int = 10, skip: int = 0, search: str = "", search_content: str = ""):
#     posts = db.query(models.Post).filter(
#     models.Post.user_id == int(current_user_id.id),
#     models.Post.title.ilike(f"%{search}%"),
#     models.Post.content.ilike(f"%{search_content}%")
#     ).limit(limit).offset(skip).all()
    
#     if posts == []:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#         detail=f"No posts found for user id {current_user_id.id}")
    
#     # Mask the emails in user_info
#     for post in posts:
#         if post.user_info:
#             email_str = post.user_info.email
#             name, domain = email_str.split('@')
#             first = name[0]
#             last = name[-1]
#             post.user_info.email = f"{first}****{last}@{domain}"


#     post_vote = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
#         models.Vote, models.Vote.post_id == models.Post.id, isouter=True
#     ).group_by(models.Post.id).all()

#     print(post_vote)
    
#     return [post_vote]


@router.get("/", response_model=list[PostWithVotes]) 
def get_posts(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: str = "",
    search_content: str = ""
):
    posts = db.query(models.Post).filter(
        models.Post.user_id == int(current_user_id.id),
        models.Post.title.ilike(f"%{search}%"),
        models.Post.content.ilike(f"%{search_content}%")
    ).limit(limit).offset(skip).all()
    
    if posts == []:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No posts found for user id {current_user_id.id}"
        )

    # Mask the emails in user_info
    for post in posts:
        if post.user_info:
            email_str = post.user_info.email
            name, domain = email_str.split("@")
            post.user_info.email = f"{name[0]}****{name[-1]}@{domain}"

    # vote count query (kept)
    post_vote = db.query(
        models.Vote.post_id,
        func.count(models.Vote.post_id).label("votes")
    ).group_by(
        models.Vote.post_id
    ).all()

    # map votes to posts
    vote_dict = {pv.post_id: pv.votes for pv in post_vote}

    for post in posts:
        post.votes = vote_dict.get(post.id, 0)

    return posts




# CREATE POST
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=CreatePost)
def create_post(post:CreatePost,db: Session = Depends(get_db),current_user_id: int = Depends(oauth2.get_current_user)):
    created_post = models.Post(user_id = current_user_id.id,**post.model_dump())
    db.add(created_post)
    db.commit() 
    db.refresh(created_post)
    return created_post


# GET SPECIFIC POST
@router.get("/id/{id}", response_model=Post)
def get_post(id: int,db: Session = Depends(get_db),current_user_id: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Post with id: {id} was not found")
    
    if post.user_id != int(current_user_id.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not authorized to perform requested action") 
    
    return post

# DELETE POST
@router.delete("/id/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),current_user_id: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id)
    deleted_post = post.first()
    # print(f"deleted_post is {deleted_post.user_id}")
    # print(f"current_user_id is {current_user_id.id}")
    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} does not exist" )
    
    if deleted_post.user_id != int(current_user_id.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not authorized to perform requested action")   
    
    post.delete(synchronize_session=False)
    db.commit()


# UPDATE POST
@router.put("/id/{id}", response_model=UpdatePost)
def update_post(id: int,post: UpdatePost, db: Session = Depends(get_db),user_id: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    update_post = post_query.first()
    post = update_post
    if update_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} does not exist")
    
    if post.user_id != oauth2.get_current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not authorized to perform requested action")
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()
