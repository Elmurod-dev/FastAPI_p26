from sqlalchemy import DECIMAL, ForeignKey
from sqlalchemy.orm import declared_attr
from sqlmodel import Field, Session, SQLModel, create_engine, select, VARCHAR, TEXT, Relationship


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



SQLALCHEMY_DATABASE_URL = "postgresql://postgres:1@localhost:5432/postgres"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SQLModel.metadata.create_all(engine)

