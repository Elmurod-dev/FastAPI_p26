from fastapi import Request
from sqlmodel import select
from app.main.conf import app, templates, SessionDep
from db.models import User


@app.get('/user/list' , name='income-form')
async def product_list(request:Request , session : SessionDep):
    users = session.exec(select(User)).fetchall()
    return templates.TemplateResponse(request , 'profile.html' , {"users" : users})





