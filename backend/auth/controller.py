from fastapi import APIRouter, Request, status, Depends
from backend.database.core import DbSession
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
import backend.auth.models as models
import backend.auth.service as service

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def register_user(request: Request, db: DbSession, register_user_request: models.RegisterUserRequest):
    service.register_user(db, register_user_request)


@router.post("/token", response_model=models.Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: DbSession):
    return service.login_for_access_token(form_data, db)