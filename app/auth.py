from datetime import datetime, timedelta

import bcrypt
from jose import JWTError, jwt

from app.config import settings


def hash_password(password: str) -> str:
    # bcrypt has a 72-byte limit
    pwd_bytes = password.encode("utf-8")[:72]
    return bcrypt.hashpw(pwd_bytes, bcrypt.gensalt()).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(
            plain.encode("utf-8")[:72],
            hashed.encode("utf-8"),
        )
    except Exception:
        return False


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.jwt_expire_minutes)
    to_encode.update({"exp": expire})
    algo = settings.jwt_algorithm.strip() or "HS256"
    return jwt.encode(to_encode, settings.jwt_secret, algorithm=algo)


def decode_access_token(token: str) -> dict | None:
    try:
        algo = settings.jwt_algorithm.strip() or "HS256"
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[algo])
        return payload
    except JWTError:
        return None
