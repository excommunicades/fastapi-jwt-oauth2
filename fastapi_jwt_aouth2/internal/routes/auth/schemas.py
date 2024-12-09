from pydantic import BaseModel, Field, EmailStr


class RegisterUserSchema(BaseModel):

    nickname: str = Field(max_length=50)

    email: EmailStr = Field(max_length=100)

    password: str = Field(max_length=255)
