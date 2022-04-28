from fastapi import Body, Depends, FastAPI, Response, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from typing import List


router = APIRouter(prefix = "/posts",tags=['Posts'])


# create one post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post )
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
    return new_post



# read all posts
@router.get("/",status_code=status.HTTP_200_OK,response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * from posts  """)
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()   # use the query method of db on models.Post table i.e the posts table and get all rows
    if not posts:
        raise HTTPException(stauts_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail = "Unable to fetch posts")
    return posts




# read a single post
@router.get("/{id}", status_code=status.HTTP_302_FOUND,response_model=schemas.Post)
def get_post(id: int,db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * from posts WHERE id = %s """,(str(id)))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} was not found")
    return post



# delete a post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
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
@router.put("/{id}",response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate,db: Session = Depends(get_db)):
    # cursor.execute(""" UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *""",(post.title,post.content,post.published,str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} was not found")
    post_query.update(updated_post.dict(),synchronize_session=False)
    
    db.commit()
    return post_query.first()
