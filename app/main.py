from email.policy import HTTP
from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange

from requests import Response


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts = [{"title":"title of post 1", "content":"content of post 1", "id": 1}, {"title":"fav foods", "content":"pizza", "id": 2} ]

def find_post(id):
     for p in my_posts:
         if p["id"] == id:
             return p

def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p['id'] == id:
            return i
    

@app.get("/")
def root():
    return {"message": "Hello World"}

# create one post
@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0,1000000)
    my_posts.append(post_dict)
    return {"new post": post_dict}

# read all posts
@app.get("/posts")
def get_posts():
    return {"data": my_posts}

# read a single post
@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(int(id))
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found")        
    return {"post_detail":post}


# delete a post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(int(id))
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found")      
    my_posts.pop(index)
    return {"msg":"deleted"}
    
    
# update a post    
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(int(id))
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found") 
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"data":post_dict}