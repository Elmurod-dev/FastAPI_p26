from datetime import timedelta, datetime

import jwt
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from passlib.context import CryptContext
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import declared_attr
from sqlalchemy.orm import sessionmaker
from sqlmodel import Field, SQLModel


class BaseSQLModel(SQLModel , abstract=True):
    id: int | None = Field(primary_key=True)
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + "s"


class User(BaseSQLModel, table=True):
    first_name: str
    last_name : str = Field(unique=True)
    job : str = Field(unique=True,nullable=True)
    address : str = Field(min_length=5,nullable=True)
    email : str = Field(min_length=5)
    phone_number : str = Field(min_length=5,nullable=True)
    password : str = Field(min_length=5)

class Job(BaseSQLModel, table=True):
    title: str = Field(nullable=True)
    job_type : str
    address : str = Field(min_length=5,nullable=True)
    company : str


# SECRET_KEY = "FASTAPI"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:1@localhost:5432/postgres"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SQLModel.metadata.create_all(engine)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# templates = Jinja2Templates(directory="templates")
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
#
# def hash_password(password: str) -> str:
#     return pwd_context.hash(password)
#
# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)
#
# def create_access_token(data: dict, expires_delta: timedelta | None = None):
#     to_encode = data.copy()
#     expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
#     to_encode.update({"exp": expire})
#     return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#
# def get_user_by_email(db: Session, email: str):
#     return db.query(User).filter(User.email == email).first()
#
# def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
#     try:
#         payload = jwt.decode(token, "FASTAPI", algorithms=["HS256"])
#         user_id: int = payload.get("sub")
#         if user_id is None:
#             raise Exception("User not found")
#     except AssertionError:
#         raise Exception("Invalid token")
#
#     user = db.query(User).filter(User.id == user_id).first()
#     return user
#
