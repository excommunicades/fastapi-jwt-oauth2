from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from fastapi_jwt_aouth2.pkg.db.repositories import (
    UserManagementRepository,
)
from fastapi_jwt_aouth2.internal.routes.auth.schemas import (
    RegisterUserSchema
)

from fastapi_jwt_aouth2.pkg.db.database import get_db

from fastapi_jwt_aouth2.pkg.jwt.jwt_settings import ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi_jwt_aouth2.pkg.jwt.repositories import JWTRepository

router = APIRouter(
    prefix='/auth',
    tags=['User Management']
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_user_service(db: Session = Depends(get_db)):

    return UserManagementRepository(db)

@router.post('/register')
def registration(data: RegisterUserSchema, userRepository: UserManagementRepository = Depends(get_user_service)):

    try:

        userRepository.register_user(nickname=data.nickname, email=data.email, password=data.password)

        return JSONResponse(
            status_code=201,
            content={
                "message": "You were registered successfully!"
            })

    except HTTPException as e:

        return JSONResponse(
            status_code=e.status_code,
            content={
                'errors': e.detail
            })


@router.post('/login')
def login(form_data: OAuth2PasswordRequestForm = Depends(), userRepository: UserManagementRepository = Depends(get_user_service)):

    try:

        user = userRepository.login_user(nickname_or_email=form_data.username, password=form_data.password)

    except HTTPException as e:

        return JSONResponse(
            status_code=e.status_code,
            content={
                'errors': e.detail
            })

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = JWTRepository.create_access_token(
        data={"sub": user.nickname}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}
