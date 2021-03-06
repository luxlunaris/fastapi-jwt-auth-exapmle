import asyncio

from fastapi import Depends, Request, Response
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from sqlalchemy.exc import IntegrityError
from starlette.responses import JSONResponse

from .app import create_app
from .config import jwt_config
from .db import Session, User
from .models import UserJSON, UserSignUpJSON
from .utils import hash_password, verify_password


app = create_app()


denylist = set()


@AuthJWT.load_config
def get_config():
    """Configuration getter for fastapi-jwt-auth"""
    return jwt_config


@AuthJWT.token_in_denylist_loader
def check_if_token_in_denylist(decrypted_token) -> bool:
    jti = decrypted_token["jti"]
    return jti in denylist


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(_: Request, exc: AuthJWTException) -> JSONResponse:
    """Exceptions formatting"""
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


@app.post("/sign-in")
async def sign_in(user: UserJSON, Authorize: AuthJWT = Depends()) -> JSONResponse:
    """Signs in user by given credentials"""
    Authorize.jwt_optional()

    current_user = Authorize.get_jwt_subject()
    if current_user is not None:
        return JSONResponse(
            {
                "message": "You have signed in already",
            },
            status_code=400,
        )

    user = user.dict()
    s = Session()
    user_entry = s.query(User).filter_by(email=user["email"]).first()
    if not user_entry or not verify_password(
        user["password"], user_entry.password_hash
    ):
        return JSONResponse(
            {
                "message": "Invalid email or password",
            },
            status_code=401,
        )

    response = JSONResponse({"message": "Authorized successfully"}, status_code=200)
    access_token = Authorize.create_access_token(subject=user["email"])
    Authorize.set_access_cookies(access_token, response=response)

    return response


@app.post("/sign-up", response_class=JSONResponse)
async def sign_up(user: UserSignUpJSON, Authorize: AuthJWT = Depends()) -> JSONResponse:
    """Signs up user by given credentials"""
    Authorize.jwt_optional()

    current_user = Authorize.get_jwt_subject()
    if current_user is not None:
        return JSONResponse(
            {
                "message": "Cannot create new user when signed in",
            },
            status_code=400,
        )

    user = user.dict()
    user["password_hash"] = hash_password(user["password"])
    del user["password"]

    s = Session()
    s.add(User(**user, role_id=1))
    try:
        s.commit()
    except IntegrityError:
        return JSONResponse(
            {
                "message": "User with such email already exists",
            },
            status_code=400,
        )

    return JSONResponse(
        {
            "message": "User has been created",
        },
        status_code=201,
    )


@app.post("/sign-out")
async def sign_out(Authorize: AuthJWT = Depends()) -> Response:
    """Signs out user if they are signed in"""
    Authorize.jwt_required()
    Authorize.unset_jwt_cookies()

    return Response(status_code=200)
