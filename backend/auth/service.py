from sqlalchemy.orm import Session
from sqlalchemy import update
import backend.auth.models as models
from backend.database.schemas.user import User, UserRole
from backend.database.schemas.password_reset import PasswordReset
from uuid import UUID, uuid4
import logging
from passlib.context import CryptContext
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, Response, Cookie
from backend.exceptions import AuthenticationError
from datetime import timedelta, datetime, timezone
import jwt
from jwt import PyJWTError, ExpiredSignatureError
from backend.database.core import SessionLocal
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv(
    "AUTH_JWT_SECRET",
    "197b2c37c391bed93fe80344fe73b806947a65e36206e05a1a23c2fa12702fe3",
)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
# 7 days
REFRESH_TOKEN_EXPIRE_MINUTES = 24 * 60 * 7

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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

    super_email = os.getenv("SUPERUSER_EMAIL", "admin@admin.com")
    super_password = os.getenv("SUPERUSER_PASSWORD", "admin")

    try:
        super_user = User(
            id=uuid4(),
            email=super_email,
            first_name="Admin",
            last_name="Admin",
            password_hash=get_password_hash(super_password),
            role=UserRole.ADMIN,
        )
        db.add(super_user)
        db.commit()
    except Exception as e:
        logging.error(f"Failed to create super user. Error {e}")
        raise
    db.close()


def register_user(
    db: Session, register_user_request: models.RegisterUserRequest
) -> None:
    try:
        role = UserRole.ADMIN if db.query(User).count() == 0 else UserRole.USER
        create_user_model = User(
            id=uuid4(),
            email=register_user_request.email,
            first_name=register_user_request.first_name,
            last_name=register_user_request.last_name,
            password_hash=get_password_hash(register_user_request.password),
            role=role,
        )
        db.add(create_user_model)
        db.commit()
    except Exception as e:
        logging.error(
            f"Failed to register user: {register_user_request.email}. Error: {str(e)}"
        )
        raise


def verify_token(token: str) -> models.TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        user_role: str = payload.get("role")
        logging.info(f"PAYLOAD: {payload}")
        return models.TokenData(user_id=user_id, user_role=user_role)
    except ExpiredSignatureError:
        logging.warning("Access token expired")
        raise AuthenticationError()
    except PyJWTError as e:
        logging.warning(f"Token verification failed: {str(e)}")
        raise AuthenticationError()


def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session,
    response: Response,
) -> models.Token:
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise AuthenticationError()
    access_token = create_access_token(
        user.id,
        user.role.value,
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    refresh_token = create_refresh_token(
        user.id,
        user.role.value,
        timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES),
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        max_age=REFRESH_TOKEN_EXPIRE_MINUTES * 60,  # 7 days
    )

    return models.Token(access_token=access_token, token_type="bearer")


def refresh(response: Response, refresh_token: str = Cookie(None)) -> models.Token:
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Missing refresh token")

    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        role = payload.get("role")
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expired")
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    access_token = create_access_token(
        user_id=user_id,
        role=role,
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    new_refresh_token = create_refresh_token(
        user_id, role, timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    )

    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        max_age=REFRESH_TOKEN_EXPIRE_MINUTES * 60,  # 7 days
    )

    return models.Token(access_token=access_token, token_type="bearer")


def authenticate_user(email: str, password: str, db: Session) -> User | None:
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password_hash):
        logging.warning(f"Failed authentication attempt for email: {email}")
        return None
    return user


def create_refresh_token(user_id: UUID, role: str, expires_delta: timedelta) -> str:
    encode = {
        "sub": str(user_id),
        "role": role,
        "exp": datetime.now(timezone.utc) + expires_delta,
    }
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def create_access_token(user_id: UUID, role: str, expires_delta: timedelta) -> str:
    encode = {
        "sub": str(user_id),
        "role": role,
        "exp": datetime.now(timezone.utc) + expires_delta,
    }
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


# TODO Generate proper code uuid?
def password_reset_token():
    return 123


from sqlalchemy.dialects.postgresql import insert


def send_password_reset_email(email: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        return AuthenticationError()

    stmt = insert(PasswordReset).values(
        user_id=user.id,
        reset_token=password_reset_token(),
        expirary_time=datetime.now(timezone.utc) + timedelta(hours=1),
    )
    stmt = stmt.on_conflict_do_update(
        index_elements=["user_id"],
        set_={
            "reset_token": password_reset_token(),
            "expirary_time": datetime.now(timezone.utc) + timedelta(hours=1),
        },
    )
    db.execute(stmt)
    db.commit()

    # TODO send email


def verify_reset_code(reset_token: str, db: Session):
    reset_req = (
        db.query(PasswordReset).filter(PasswordReset.reset_token == reset_token).first()
    )

    if reset_req is None:
        # TODO reset doesnt exist
        raise AuthenticationError()

    tz_expirary_time = reset_req.expirary_time.replace(tzinfo=timezone.utc)
    if datetime.now(timezone.utc) > tz_expirary_time:
        # TODO reset timed out
        raise AuthenticationError
    else:
        return True


def reset_password(reset_token: str, new_password: str, db: Session):
    reset_req = (
        db.query(PasswordReset).filter(PasswordReset.reset_token == reset_token).first()
    )
    if reset_req is None:
        # TODO reset doesnt exist
        raise AuthenticationError()

    tz_expirary_time = reset_req.expirary_time.replace(tzinfo=timezone.utc)
    if datetime.now(timezone.utc) > tz_expirary_time:
        # TODO reset timed out
        raise AuthenticationError

    user = db.query(User).filter(User.id == reset_req.user_id).first()
    if user is None:
        # user not in db?
        raise AuthenticationError

    new_password_hashed = get_password_hash(new_password)

    stmt = (
        update(User).where(User.id == user.id).values(password_hash=new_password_hashed)
    )
    db.execute(stmt)

    r_stmt = (
        update(PasswordReset)
        .where(PasswordReset.reset_token == reset_token)
        .values(expirary_time=datetime.now(timezone.utc))
    )
    db.execute(r_stmt)

    db.commit()
