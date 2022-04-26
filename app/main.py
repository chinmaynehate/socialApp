from email.policy import HTTP
from os import stat
from typing import Optional
from fastapi import Body, Depends, FastAPI, Response, status, HTTPException
from pkg_resources import yield_lines
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models, schemas
from app.database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)

app = FastAPI()






# connecting to the database
while True:
    try:
        conn = psycopg2.connect(host='localhost',database='socialApp',user='postgres',password='cdnsdn',cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        time.sleep(2)
        print("Connection to database failed")
        print(f"Error: {error}")


@app.get("/home")
def root():
    return {"message": "Hello World"}

# create one post
@app.post("/posts", status_code=status.HTTP_201_CREATED, )
def create_posts(post: schemas.PostCreate,db: Session = Depends(get_db)):
    # cursor.execute(""" INSERT into posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,(post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(**post.dict()) #title=post.title,content=post.content,published=post.published
    db.add(new_post) # add the post to db
    db.commit() # commit it i.e save it
    db.refresh(new_post) # retrieve it and store it back into new_post
    if not new_post:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    return {"new post": new_post}

# read all posts
@app.get("/posts",status_code=status.HTTP_200_OK)
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * from posts  """)
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()   # use the query method of db on models.Post table i.e the posts table and get all rows
    if not posts:
        raise HTTPException(stauts_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail = "Unable to fetch posts")
    return {"data": posts}

# read a single post
@app.get("/posts/{id}", status_code=status.HTTP_302_FOUND)
def get_post(id: int,db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * from posts WHERE id = %s """,(str(id)))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} was not found")
    return {"post_detail": post}


# delete a post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute(""" DELETE from posts WHERE id = %s RETURNING *""",(str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} was not found")
    post.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# update a post
@app.put("/posts/{id}")
def update_post(id: int, updated_post: schemas.PostCreate,db: Session = Depends(get_db)):
    # cursor.execute(""" UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *""",(post.title,post.content,post.published,str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} was not found")
    post_query.update(updated_post.dict(),synchronize_session=False)
    
    db.commit()
    return {"data": post_query.first()}



