from pydantic import BaseModel



# Pydantic model of the post
# they define the structure of request and response

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    
class PostCreate(PostBase):
    pass
    