from django.contrib.auth import authenticate
from ninja import Form, Router, Schema
from ninja.security import HttpBearer

from apps.users.models import Token

router = Router()


class GlobalAuth(HttpBearer):
    def authenticate(self, request, token):
        try:
            return Token.objects.get(token=token).user
        except Token.DoesNotExist:
            pass


class AuthSchema(Schema):
    email: str
    password: str


@router.post("/authenticate", auth=None)  # overriding global auth
def get_token(request, auth_data: AuthSchema):
    user = authenticate(username=auth_data.email, password=auth_data.password)
    if user:
        # Assuming a user can have multiple tokens and you want to create a new one every time
        new_token = Token.objects.create(user=user)
        return {"token": new_token.token, "expires": new_token.expiry_as_iso8601}
    else:
        return {"error": "Invalid credentials"}, 401
