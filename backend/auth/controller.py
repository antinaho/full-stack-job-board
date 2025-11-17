from fastapi import APIRouter, status, Depends, Cookie, Response, Query
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
import backend.auth.models as models
import backend.auth.service as service
from backend.deps import DbSessionDep
from pydantic import EmailStr


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(
    db: DbSessionDep,
    register_user_request: models.RegisterUserRequest,
):
    service.register_user(db, register_user_request)


@router.post("/login", response_model=models.Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: DbSessionDep,
    response: Response,
):
    return service.login(form_data, db, response)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout_user(response: Response):
    response.delete_cookie(key="refresh_token")
    return models.GenericMessage(msg="logut successful")


@router.post("/refresh", response_model=models.Token)
async def refresh(response: Response, refresh_token: str = Cookie(None)):
    return service.refresh(response, refresh_token)


# TODO return something more describtive from all of these
@router.post("/forgot-password", response_model=models.GenericMessage)
def send_password_reset_email(
    email: Annotated[EmailStr, Query()], db: DbSessionDep
) -> models.GenericMessage:
    service.send_password_reset_email(email, db)
    return models.GenericMessage(msg="Email reset send")


@router.post("/reset-password")  # For users who lost password
def reset_password(
    reset_code: Annotated[str, Query()],
    new_password: Annotated[str, Query()],
    db: DbSessionDep,
) -> models.GenericMessage:
    service.reset_password(reset_code, new_password, db)
    return models.GenericMessage(msg="Password reset")


@router.post("/verify-reset-code")  # For frontend rendering
def verify_reset_code(
    reset_code: Annotated[str, Query()], db: DbSessionDep
) -> models.GenericMessage:
    service.verify_reset_code(reset_code, db)
    return models.GenericMessage(msg="Code valid")
