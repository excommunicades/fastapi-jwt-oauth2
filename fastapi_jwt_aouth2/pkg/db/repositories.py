import bcrypt
from sqlalchemy.orm import Session

from fastapi import HTTPException
from fastapi.responses import JSONResponse

from fastapi_jwt_aouth2.pkg.db.models import User

class UserManagementRepository:

    def __init__(self, db: Session):

        self.db = db
        # self.jwt_repository = JWT

    def register_user(self, nickname: str, email: str, password: str) -> User:

        if self.db.query(User).filter_by(nickname=nickname).first():

            raise HTTPException(status_code=400, detail='User with this nickname already exist!')

        if self.db.query(User).filter_by(email=email).first():

            raise HTTPException(status_code=400, detail='User with this email already exist!')

        salt = bcrypt.gensalt()

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

        user = User(nickname=nickname, email=email, password= hashed_password)

        self.db.add(user)
        self.db.commit()

        return user

    def login_user(self, nickname_or_email: str, password: str,) -> JSONResponse:

        user = self.db.query(User).filter_by(nickname=nickname_or_email).first()

        if not user:

            self.db.query(User).filter_by(email=nickname_or_email).first()

            if not user:

                raise HTTPException(status_code=404, detail='User does not exist.')

        hashed_password = bytes.fromhex(user.password[2:])

        print(hashed_password)
        print(bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()))

        if not bcrypt.checkpw(password.encode('utf-8'), hashed_password):

            raise HTTPException(status_code=401, detail="Incorrect password")

        return user
