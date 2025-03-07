import hashlib

from pydantic import BaseModel, field_validator

from app.main.conf import SessionDep
from db.models import User


class UserForm(BaseModel):
    name : str
    age : int


class RegisterForm(BaseModel):
    first_name : str
    last_name : str
    email : str
    password : str

    @field_validator('password')
    @classmethod
    def hash_password(cls, value: str) -> str:
        value = hashlib.sha256(value.encode())
        return value.hexdigest()

    def save(self, session : SessionDep):
        session.add(User(**self.__dict__))
        session.commit()
