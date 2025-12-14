from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from . import schemas
from fastapi import Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordBearer
from .config import settings    

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')  

#SECRET KEY
#ALGO
#Expiration time

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# def verify_access_token(token: str, credentials_exception):
#     try:    
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])       
#         user_id = payload.get("user_id") 

#         if user_id is None:
#             raise credentials_exception 

#         token_data = schemas.TokenData(id=str(user_id))
#         return token_data
    
#     except JWTError:
#         raise credentials_exception


def verify_access_token(token: str, credentials_exception):
    try:    
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])       
        id = payload.get("user_id") 

        if id is None:
            raise credentials_exception 
        token_data = schemas.TokenData(id=str(id))
        return token_data
    
    except JWTError:
        raise credentials_exception
    








def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"})
    
    return verify_access_token(token, credentials_exception)





