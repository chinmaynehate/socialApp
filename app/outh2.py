from jose import JWTError, jwt
from datetime import datetime, timedelta

# SECRET KEY
# ALGORITHM that is to be used
# Expiration time for a user to stay logged in

SECRET_KEY = "c882635be93f825ea255543c92bd39298b9dcfc0254129b4948cbbce1c0631e8"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt