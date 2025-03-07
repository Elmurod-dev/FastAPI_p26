import bcrypt
from starlette.requests import Request
from starlette.responses import Response
from starlette_admin.auth import AdminConfig, AdminUser, AuthProvider
from starlette_admin.exceptions import FormValidationError, LoginFailed




class UsernameAndPasswordProvider(AuthProvider):

    async def login(
        self,
        username: str,
        password: str,
        remember_me: bool,
        request: Request,
        response: Response) -> Response:
        if len(username) < 3:
            """Form data validation"""
            raise FormValidationError(
                {"username": "Ensure username has at least 03 characters"}
            )

        if username == 'admin' and bcrypt.checkpw(password.encode() , "$2b$12$IK.O9qcAqfvyO5v1NmZiW.f6nIVyGPQZFwVfm2jjbyl0wQA7GXFNi".encode()):
            """Save `username` in session"""
            request.session.update({"username": username})
            return response

        raise LoginFailed("Invalid username or password")

    async def is_authenticated(self, request) -> bool:
        if request.session.get("username", None) == 'admin':
            username = request.session["username"]
            request.state.user = username
            return True
        return False

    def get_admin_config(self, request: Request) -> AdminConfig:
        return AdminConfig(
            app_title="Factor Bot Admin"
        )

    def get_admin_user(self, request: Request) -> AdminUser:
        user = request.state.user  # Retrieve current user
        print(user, "====================================================")
        return AdminUser(username=user)

    async def logout(self, request: Request, response: Response) -> Response:
        request.session.clear()
        return response