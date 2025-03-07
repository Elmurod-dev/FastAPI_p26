from fastapi import Depends, Form
from fastapi import Request
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER

from app.main.conf import app, templates, SessionDep
from app.serializers import RegisterForm, ProfileForm
from db.models import User


@app.get('/register')
async def register_template(request : Request):
    return templates.TemplateResponse(request , 'auth/register.html' )

@app.post('/register/post',name='register')
async def register_form(request : Request ,session : SessionDep, user : RegisterForm = Form(...)):
    user.save(session)
    return RedirectResponse('/login' , status_code=HTTP_303_SEE_OTHER)

#
# @app.get("/login", response_class=HTMLResponse)
# async def login_page(request: Request):
#     return templates.TemplateResponse("auth/login.html", {"request": request})
#
#
# @app.post("/login")
# async def login(
#         request: Request,
#         email: str = Form(...),
#         password: str = Form(...),
#         db: Session = Depends(get_db)
# ):
#     user = get_user_by_email(db, email)
#     if not user or not verify_password(password, user.password):
#         return templates.TemplateResponse("auth/login.html", {"request": request, "error": "Invalid email or password"})
#
#     token = create_access_token(data={"sub": user.email})
#
#     response = RedirectResponse(url="/profile/update", status_code=303)
#     response.set_cookie(key="access_token", value=token)
#     return response
#
# @app.get("/logout")
# async def logout():
#     response = RedirectResponse(url="/login")
#     response.delete_cookie("access_token")
#     return response
@app.get('/profile/update/{id}', response_class=HTMLResponse)
async def profile_update(request: Request, id:int,session : SessionDep):
    user = session.query(User).filter(User.id == id).first()
    return templates.TemplateResponse("homework/profileupdate.html", {"request": request, "user": user})


@app.post('/profile/post/{id}',name='update')
async def register_form(request : Request ,id:int,session : SessionDep, user : ProfileForm = Form(...)):
    user_ = session.query(User).filter(User.id == id).first()
    if not user_:
        return HTMLResponse("<h1>User not found</h1>", status_code=404)
    user_data = user.model_dump()
    for key, value in user_data.items():
        setattr(user_, key, value)
    session.commit()
    return RedirectResponse('/user/list' , status_code=HTTP_303_SEE_OTHER)