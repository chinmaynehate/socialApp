from email.policy import default
from xmlrpc.client import Boolean
from app.database import Base
from sqlalchemy import TIMESTAMP, Column, Integer, String ,Boolean
from sqlalchemy.sql.expression import text


# for posts table in dataase
class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='True',nullable=False)
    created_at  = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    
    
    