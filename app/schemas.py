from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint

class PostBase(BaseModel):
    title:str
    content:str
    published:bool=True
    
class PostCreate(PostBase):
   pass
  
  
class UserCreate(BaseModel):
    email:EmailStr
    password:str
    
class UserOut(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime   

    class config:
        orm_mode=True  

class Post(BaseModel):
    id:int
    title:str
    content:str
    published:bool=True    
    created_at:datetime
    
    
    
    class config:
        orm_mode=True
        
        

        
class UserLogin(BaseModel):
    email:EmailStr
    password:str
    
    
class Token(BaseModel):
    access_token:str
    token_type:str
    
class TokenData(BaseModel):
    id:Optional[str]=None
    email:EmailStr=None

    
class Vote(BaseModel):
    post_id:int
    dir:int=conint(le=1)
    
class Book(BaseModel):
    title:str
    description:str