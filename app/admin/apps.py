import uvicorn
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette_admin.contrib.sqla import Admin, ModelView

from app.admin.provider import UsernameAndPasswordProvider
from db.models import engine, User

app = Starlette()

admin = Admin(engine=engine,
              title="Example: SQLAlchemy",
              base_url='/',
              auth_provider=UsernameAndPasswordProvider(),
              middlewares=[Middleware(SessionMiddleware, secret_key="qewrerthytju4")])

class AllModelView(ModelView):
    exclude_fields_from_create = ["created_at" , 'updated_at']
admin.add_view(AllModelView(User))

admin.mount_to(app)

if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8001)


