"""hyperglass API middleware."""

# Standard Library
import os
import typing as t

import jwt
from litestar.config.compression import CompressionConfig

# Third Party
from litestar.config.cors import CORSConfig
from litestar.connection import ASGIConnection
from litestar.exceptions import NotAuthorizedException
from litestar.middleware import AbstractAuthenticationMiddleware, AuthenticationResult

from hyperglass.log import log

if t.TYPE_CHECKING:
    # Project
    from hyperglass.state import HyperglassState

__all__ = ("create_cors_config", "COMPRESSION_CONFIG")

COMPRESSION_CONFIG = CompressionConfig(backend="brotli", brotli_gzip_fallback=True)

REQUEST_LOG_MESSAGE = "REQ"
RESPONSE_LOG_MESSAGE = "RES"
REQUEST_LOG_FIELDS = ("method", "path", "path_params", "query")
RESPONSE_LOG_FIELDS = ("status_code",)


class CustomAuthMiddleware(AbstractAuthenticationMiddleware):
    async def authenticate_request(
        self, connection: ASGIConnection
    ) -> AuthenticationResult:
        token = connection.cookies.get("access_token")
        secret_key = os.getenv("SECRET_KEY")

        log.debug("Entering authenticate middleware")

        if not token:
            raise NotAuthorizedException(detail="Not authenticated")

        log.debug(f"token {token}")

        try:
            jwt.decode(token, secret_key, algorithms=["HS256"])
        except jwt.ExpiredSignatureError as err:
            raise NotAuthorizedException(detail="Expired token") from err
        except jwt.InvalidTokenError as err:
            raise NotAuthorizedException(detail="Invalid token") from err

        return AuthenticationResult(user=None, auth=token)


def create_cors_config(state: "HyperglassState") -> CORSConfig:
    """Create CORS configuration from parameters."""
    origins = state.params.cors_origins.copy()
    if state.settings.dev_mode:
        origins = [*origins, state.settings.dev_url, "http://localhost:3000"]

    return CORSConfig(
        allow_origins=origins,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["*"],
    )
