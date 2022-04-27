from fastapi import Body, Depends, FastAPI, Response, status, HTTPException, APIRouter
from sqlalchemy.orm import Session

from app import routers
from .. import models, schemas, utils
from ..database import get_db
from typing import List



router = APIRouter(prefix = "/users")

# create user
@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_posts(user: schemas.UserCreate,db: Session = Depends(get_db)):
    # cursor.execute(""" INSERT into posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,(post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    
    # hashing the password
    user.password = utils.hash(user.password)
    new_user = models.User(**user.dict()) #title=post.title,content=post.content,published=post.published
    db.add(new_user) # add the post to db
    db.commit() # commit it i.e save it
    db.refresh(new_user) # retrieve it and store it back into new_post
    if not new_user:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    return new_user

# get one user
@router.get("/{id}",status_code=status.HTTP_302_FOUND,response_model=schemas.UserOut)
def get_user(id: int,db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id: {id} not found")
    return user
    