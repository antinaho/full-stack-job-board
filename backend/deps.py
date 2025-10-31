from backend.database.core import SessionLocal
from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from backend.auth.service import verify_token
from fastapi.security import OAuth2PasswordBearer
import backend.auth.models as auth_model
from backend.exceptions import AuthenticationError


def get_db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


DbSessionDep = Annotated[Session, Depends(get_db)]

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_user(
    token: Annotated[str, Depends(oauth2_bearer)],
) -> auth_model.TokenData:
    return verify_token(token)


CurrentUser = Annotated[auth_model.TokenData, Depends(get_current_user)]


def require_role(required_role: str):
    def role_checker(current_user: auth_model.TokenData = Depends(get_current_user)):
        if current_user.user_role != required_role:
            raise AuthenticationError
        return current_user

    return role_checker


CurrentAdminUser = Annotated[auth_model.TokenData, Depends(require_role("admin"))]
