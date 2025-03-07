
from sqlmodel import select
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER

from app.main.conf import app, templates, SessionDep
from fastapi import Request, Form

from app.serializers import RegisterForm


@app.get('/register')
async def register_template(request : Request):
    return templates.TemplateResponse(request , 'auth/register.html' )

@app.post('/register/post',name='register')
async def register_form(request : Request ,session : SessionDep, user : RegisterForm = Form(...)):
    user.save(session)
    return RedirectResponse('/user/list' , status_code=HTTP_303_SEE_OTHER)
