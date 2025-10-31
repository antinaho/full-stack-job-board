from fastapi import APIRouter, Request, status, Depends, Cookie, Response
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
import backend.auth.models as models
import backend.auth.service as service
from backend.deps import DbSessionDep

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def register_user(
    request: Request,
    db: DbSessionDep,
    register_user_request: models.RegisterUserRequest,
):
    service.register_user(db, register_user_request)


@router.post("/token", response_model=models.Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: DbSessionDep,
    response: Response,
):
    return service.login_for_access_token(form_data, db, response)


@router.post("/refresh", response_model=models.Token)
async def login_for_refresh_token(
    response: Response, refresh_token: str = Cookie(None)
):
    return service.login_for_refresh_token(response, refresh_token)
