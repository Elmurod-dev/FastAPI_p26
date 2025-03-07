# from typing import Annotated
#
# from fastapi import Form
#
# from app.main.conf import app, SessionDep
# from app.serializers import UserForm
# from db.models import engine, User , select
#
# @app.get("/")
# async def root():
#     return {"message": "Hello World"}
#
# @app.get("/hello/{name}")
# async def say_hello(name: str):
#     return {"message": f"Hello {name}"}
#
#
# @app.post("/user/create")
# async def user_create( session : SessionDep ,user: UserForm = Form(...)):
#     user = User(**user.__dict__)
#     session.add(user)
#     session.commit()
#     session.refresh(user)
#     return {"message":user}
#
#
#
# @app.put("/user/update")
# async def user_updade(user_id : int , session: SessionDep , user: UserForm = Form(...)):
#     user_obj = session.get(User, user_id)
#     if not user:
#         raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail="User not found")
#     form_dict = user.model_dump(exclude_unset=True)
#     for attr , value in form_dict.items():
#         setattr(user_obj , attr , value)
#     session.add(user_obj)
#     session.commit()
#     session.refresh(user_obj)
#     return user_obj
#
#
#
#
# # -----------------------
#
# # pip install fastapi uvicorn python-jose[cryptography] passlib
#
#
# from datetime import datetime, timedelta
# from typing import Optional
# from fastapi import FastAPI, Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from jose import JWTError, jwt
# from passlib.context import CryptContext
# SECRET_KEY = "zqxwcevrbtynumikol123456765432"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# def verify_password(plain_password, hashed_password):
#     # return pwd_context.verify(plain_password, hashed_password)
#     return plain_password == hashed_password
# def get_password_hash(password):
#     return pwd_context.hash(password)
# def get_user(session:SessionDep, username: str):
#     query = session.exec(select(User).where(User.username == username))
#     user = query.fetchall()
#     if user:
#         return user[0]
# # Token yaratish
# def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
#     to_encode = data.copy()
#     expire = datetime.now() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt
# async def get_current_user(session: SessionDep ,token: str = Depends(oauth2_scheme)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Invalid authentication credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#     except JWTError:
#         raise credentials_exception
#
#     user = get_user(session, username)
#     if user is None:
#         raise credentials_exception
#     return user
#
# @app.post("/token")
# async def login(session :SessionDep ,form_data: OAuth2PasswordRequestForm = Depends() ):
#     user = get_user(session, form_data.username)
#     if not user or not verify_password(form_data.password, user.password):
#         raise HTTPException(status_code=400, detail="Incorrect username or password")
#
#     access_token = create_access_token(data={"sub": user.username})
#     return {"access_token": access_token, "token_type": "bearer"}
#
# @app.get("/users/me")
# async def read_users_me(current_user: dict = Depends(get_current_user)):
#     return current_user
