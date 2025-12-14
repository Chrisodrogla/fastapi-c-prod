from pydantic import BaseModel, ConfigDict, EmailStr, conint
from datetime import datetime
from typing import Optional

class Post(BaseModel):
    id: int
    title: str
    content: str
    published: bool = True
    created_at: datetime
    rating: int
    user_info: Optional['UserOut']
    model_config = ConfigDict(from_attributes=True)


class PostWithVotes(Post):
    votes: int = 0
    user_info: Optional['UserOut']

    model_config = ConfigDict(from_attributes=True)



class CreatePost(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: int
    id: Optional[int] = None
    model_config = ConfigDict(from_attributes=True)
    


class UpdatePost(BaseModel):
    title: str
    content: str
    rating: int


# class UpdatePost(Post):
#     title: str
#     content: str
#     published: bool = True 
#     id: Optional[int] = None
    
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

class UserLogin(BaseModel):
    email: EmailStr
    password: str    


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1) # type: ignore # 1 for upvote, 0 for remove vote    