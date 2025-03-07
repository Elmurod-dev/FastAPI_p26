from typing import Annotated
from fastapi import FastAPI, Depends
from sqlmodel import Session
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from db.models import engine

app = FastAPI()
def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
