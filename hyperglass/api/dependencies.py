import os

import jwt
from litestar import Request
from litestar.exceptions import HTTPException


async def authenticate(request: Request) -> None:
    """Authenticate user using PCI's Secret Key."""
    token = request.cookies.get("access_token")
    secret_key = os.getenv("SECRET_KEY")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        jwt.decode(token, secret_key, algorithms=["HS256"])
    except jwt.ExpiredSignatureError as err:
        raise HTTPException(status_code=401, detail="Expired token") from err
    except jwt.InvalidTokenError as err:
        raise HTTPException(status_code=401, detail="Invalid token") from err
