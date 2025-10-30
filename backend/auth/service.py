from sqlalchemy.orm import Session
import backend.auth.models as models
from backend.database.schemas.user import User, UserRole
from uuid import UUID, uuid4
import logging
from passlib.context import CryptContext
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status, Response, Cookie
from backend.exceptions import AuthenticationError
from datetime import timedelta, datetime, timezone
import jwt
from jwt import PyJWTError, ExpiredSignatureError
from backend.database.core import SessionLocal

SECRET_KEY = '197b2c37c391bed93fe80344fe73b806947a65e36206e05a1a23c2fa12702fe3'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 15
# 7 days
REFRESH_TOKEN_EXPIRE_MINUTES = 24 * 60 * 7

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return bcrypt_context.hash(password)


def register_super_user() -> None:

    db = SessionLocal()
    count = db.query(User).count()
    if count > 0:
        db.close()
        return

    try:
        super_user = User(
            id = uuid4(),
            email = "test@admin.com",
            first_name = "Markus",
            last_name = "Admin",
            password_hash = get_password_hash("password123"),
            role = UserRole.ADMIN
        )
        db.add(super_user)
        db.commit()
    except Exception as e:
        logging.error(f"Failed to create super user.")
        raise
    db.close()


def register_user(db: Session, register_user_request: models.RegisterUserRequest) -> None:
    try:
        role = UserRole.ADMIN if db.query(User).count() == 0 else UserRole.USER
        create_user_model = User(
            id=uuid4(),
            email=register_user_request.email,
            first_name=register_user_request.first_name,
            last_name=register_user_request.last_name,
            password_hash=get_password_hash(register_user_request.password),
            role = role
        )    
        db.add(create_user_model)
        db.commit()
    except Exception as e:
        logging.error(f"Failed to register user: {register_user_request.email}. Error: {str(e)}")
        raise


def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]) -> models.TokenData:    
    return verify_token(token)

CurrentUser = Annotated[models.TokenData, Depends(get_current_user)]

def verify_token(token: str) -> models.TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("id")
        user_role: str = payload.get("role")
        logging.info(f"PAYLOAD: {payload}")
        return models.TokenData(user_id=user_id, user_role=user_role)
    except ExpiredSignatureError:
        logging.warning("Access token expired")
        raise AuthenticationError()
    except PyJWTError as e:
        logging.warning(f"Token verification failed: {str(e)}")
        raise AuthenticationError()


def require_role(required_role: str):
    def role_checker(current_user: models.TokenData = Depends(get_current_user)):
        if current_user.user_role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"{required_role.capitalize()} privileges required"
            )
        return current_user
    return role_checker


def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session, response: Response) -> models.Token:
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise AuthenticationError()
    access_token = create_access_token(user.email, user.id, user.role.value, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh_token = create_refresh_token(user.email, user.id, user.role.value, timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES))
    
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        max_age=REFRESH_TOKEN_EXPIRE_MINUTES * 60 # 7 days
    )
    
    return models.Token(access_token=access_token, token_type='bearer')


def login_for_refresh_token(response: Response, refresh_token: str = Cookie(None)) -> models.Token:
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Missing refresh token")
    
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("id")
        role = payload.get("role")
        email = payload.get("sub")
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expired")
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    access_token = create_access_token(
        email=email,
        user_id=user_id,
        role=role,
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    new_refresh_token = create_refresh_token(email, user_id, role, timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES))
    
    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        max_age=REFRESH_TOKEN_EXPIRE_MINUTES * 60 # 7 days
    )

    return models.Token(access_token=access_token, token_type='bearer')


def authenticate_user(email: str, password: str, db: Session) -> User | bool:
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password_hash):
        logging.warning(f"Failed authentication attempt for email: {email}")
        return False
    return user


def create_refresh_token(email: str, user_id: UUID, role: str, expires_delta: timedelta) -> str:
    encode = {
        'sub': email,
        'id': str(user_id),
        'role': role,
        'exp': datetime.now(timezone.utc) + expires_delta
    }
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def create_access_token(email: str, user_id: UUID, role: str, expires_delta: timedelta) -> str:
    encode = {
        'sub': email,
        'id': str(user_id),
        'role': role,
        'exp': datetime.now(timezone.utc) + expires_delta

    }
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)