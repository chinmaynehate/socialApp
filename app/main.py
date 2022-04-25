from email.policy import HTTP
from os import stat
from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time


app = FastAPI()

# Pydantic model of the post
class Post(BaseModel):
    title: str
    content: str
    published: bool = True

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
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute(""" INSERT into posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,(post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    if not new_post:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    return {"new post": new_post}

# read all posts
@app.get("/posts",status_code=status.HTTP_200_OK)
def get_posts():
    cursor.execute(""" SELECT * from posts  """)
    posts = cursor.fetchall()
    if not posts:
        raise HTTPException(stauts_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail = "Unable to fetch posts")
    return {"data": posts}

# read a single post
@app.get("/posts/{id}", status_code=status.HTTP_302_FOUND)
def get_post(id: int):
    cursor.execute(""" SELECT * from posts WHERE id = %s """,(str(id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} was not found")
    return {"post_detail": post}


# delete a post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute(""" DELETE from posts WHERE id = %s RETURNING *""",(str(id)))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} was not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# update a post
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute(""" UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *""",(post.title,post.content,post.published,str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} was not found")
    return {"data": updated_post}
