from datetime import datetime, timedelta
from jose import JWTError, jwt

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import HTTPException

from fastapi_jwt_aouth2.pkg.jwt.jwt_settings import SECRET_KEY, ALGORITHM

class JWTRepository:

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=15)):

        to_encode = data.copy()

        if expires_delta:

            expire = datetime.utcnow() + expires_delta
        else:

            expire = datetime.utcnow() + timedelta(minutes=15)

        to_encode.update({'exp': expire})

        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

        return encoded_jwt

    @staticmethod
    def verify_token(token: str):

        try:

            payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)

            return payload

        except JWTError:

            raise HTTPException(status_code=401, detail="Invalid token")
