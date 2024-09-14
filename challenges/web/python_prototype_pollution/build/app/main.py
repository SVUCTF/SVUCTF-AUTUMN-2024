import os
from typing import Dict, List, Optional

import jwt
from pydantic import BaseModel
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse


app = FastAPI(openapi_url=None)
SECRET_KEY: str = os.urandom(32).hex()
FLAG = os.environ.get("GZCTF_FLAG", "SVUCTF{test_flag}")


class User(BaseModel):
    username: str
    password: str

    def get_info(self):
        return f"User: {self.username}"


class LoginRequest(BaseModel):
    username: str
    password: str


users_db: List[User] = [
    User(username="admin", password=os.urandom(32).hex()),
    User(username="user", password="123456"),
]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def merge(src, dst) -> None:
    for k, v in src.items():
        if isinstance(dst, dict):
            if dst.get(k) and isinstance(v, dict):
                merge(v, dst.get(k))
            else:
                dst[k] = v
        elif hasattr(dst, k) and isinstance(v, dict):
            merge(v, getattr(dst, k))
        else:
            setattr(dst, k, v)


def get_user(username: str) -> Optional[User]:
    return next((user for user in users_db if user.username == username), None)


def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.PyJWTError as e:
        raise HTTPException(status_code=401, detail="Invalid token") from e


app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def read_index():
    return FileResponse("static/index.html")


@app.post("/api/login")
async def login(login_data: LoginRequest):
    user = get_user(login_data.username)
    if not user or user.password != login_data.password:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    token = jwt.encode(
        {"sub": user.username, "role": "user"}, SECRET_KEY, algorithm="HS256"
    )
    return {"access_token": token, "token_type": "bearer"}


@app.post("/api/update_user")
async def update_user(user_update: Dict, token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)

    username = payload.get("sub")
    if not username:
        raise HTTPException(status_code=404, detail="User not found")

    user = get_user(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    merge(user_update, user)

    new_token = jwt.encode(
        {"sub": user.username, "role": payload.get("role", "user")},
        SECRET_KEY,
        algorithm="HS256",
    )

    return {"message": "User updated successfully", "new_token": new_token}


@app.get("/api/get_flag")
async def get_flag(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    role = payload.get("role")

    if not role or role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    return {"flag": FLAG}


# @app.get("/debug")
# async def debug():
#     return {
#         "secret_key": SECRET_KEY,
#         "users_db": [user.model_dump() for user in users_db],
#     }
