from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class AccountSchema(BaseModel):
    firstname: str = Field(...)
    lastname: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "firstname": "John",
                "lastname": "Doe",
                "email": "john.doe@yopmail.com",
                "password": "ler123",
            }
        }


class UpdateAccountModel(BaseModel):
    firstname: Optional[str]
    lastname: Optional[str]
    email: Optional[EmailStr]
    paswword: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "firstname": "John",
                "lastname": "Doe",
                "email": "john.doe@yopmail.com",
                "password": "ler123",
            }
        }


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}