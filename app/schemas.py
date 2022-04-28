from datetime import datetime
import email
from pydantic import BaseModel, EmailStr



# Pydantic model of the post
# Defines the structure of the REQUEST that is sent by the client to API
# Defines the structure of the RESPONSE that is sent by the API to client


# for /posts

# request pydantic model
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    
# this defines the exact structure of the create request. The user will have to send the data as per this class    
class PostCreate(PostBase):
    pass

# response pydantic model
class Post(PostBase):
    id : int
    created_at: datetime

    class Config:
        orm_mode = True
        
        
        
# for /users
            
# pydantic request model for user
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    
# pydantic response model for user
class UserOut(BaseModel):
    id: int
    created_at: datetime
    email: EmailStr
    
    class Config:
        orm_mode=True
        
        
        
# for /login

# pydantic model for sending a login request to the API
class UserLogin(BaseModel):
    email: EmailStr
    password: str