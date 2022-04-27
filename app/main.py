from email.policy import HTTP
from os import stat
from typing import List, Optional
from fastapi import Body, Depends, FastAPI, Response, status, HTTPException
from pkg_resources import yield_lines
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models, schemas, utils
from app.database import engine, SessionLocal, get_db
from .routers import post, user

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


app.include_router(post.router)
app.include_router(user.router)



@app.get("/home")
def root():
    return {"message": "Hello World"}




