from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

from src.config import settings

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)

        if credentials is None:
            raise HTTPException(status_code=401, detail="Not authenticated")

        if credentials.scheme != "Bearer":
            raise HTTPException(status_code=401, detail="Invalid auth scheme")

        token = credentials.credentials

        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM],
            )
            user_id = payload.get("sub")
            if not user_id:
                raise HTTPException(status_code=401, detail="Invalid token")

            return user_id   # 👈 ONLY RETURN USER ID

        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")
