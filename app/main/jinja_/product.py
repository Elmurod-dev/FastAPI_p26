import jwt
from fastapi import Request, HTTPException
from sqlmodel import select, Session
from starlette.responses import RedirectResponse, HTMLResponse

from app.main.conf import app, templates, SessionDep
from db.models import User, Job


@app.get('/user/list' , name='income-form')
async def product_list(request:Request , session : SessionDep):
    # token = request.cookies.get("access_token")
    # if not token:
    #     return RedirectResponse(url="/login")
    #
    # try:
    #     payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    #     email: str = payload.get("sub")
    #     if email is None:
    #         raise HTTPException(status_code=401, detail="Invalid token")
    # except jwt.ExpiredSignatureError:
    #     return RedirectResponse(url="/login")
    # except jwt.InvalidTokenError:
    #     return RedirectResponse(url="/login")

    users = session.exec(select(User)).fetchall()
    return templates.TemplateResponse(request , 'profile.html' , {"users" : users})

@app.get('/job/list')
async def job_list(request : Request , session : SessionDep):
    jobs = session.exec(select(Job)).fetchall()
    return templates.TemplateResponse(request , 'homework/jobs.html' , {"jobs" : jobs})





