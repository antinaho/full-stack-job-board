from fastapi import APIRouter, status, Depends, Cookie, Response, Query
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
import backend.auth.models as models
import backend.auth.service as service
from backend.deps import DbSessionDep
from backend.deps import CurrentUser
from pydantic import EmailStr, BaseModel


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


class GenericMessage(BaseModel):
    msg: str


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout_user(response: Response):
    response.delete_cookie(key="refresh_token")
    return {"status": "success"}


@router.post("/refresh", response_model=models.Token)
async def refresh(response: Response, refresh_token: str = Cookie(None)):
    return service.refresh(response, refresh_token)


@router.post("/forgot-password", response_model=GenericMessage)
def send_password_reset_email(email: Annotated[EmailStr, Query()], db: DbSessionDep):
    # Check email in db
    # Generate token
    # Save token to db with timer
    # Send token to email

    return GenericMessage(msg="Email reset send")


@router.post("verify-reset-code")
def verify_reset_code(reset_code: Annotated[str, Query()], db: DbSessionDep):
    # chck reset code is valid
    # if not return 400/401
    return GenericMessage(msg="Code valid")


@router.post("reset-password")
def reset_password(
    reset_code: Annotated[str, Query()],
    new_password: Annotated[str, Query()],
    db: DbSessionDep,
):
    # verify code still valid
    # hash new password
    # update hash in db
    # mark reset token as used
    return GenericMessage(msg="Password reset")
