from typing import Optional
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response
from .api.deps import get_current_user_optional
from .database import SessionLocal

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        db = SessionLocal()
        try:
            request.state.user = await get_current_user_optional(request, db)
            response = await call_next(request)
            return response
        finally:
            db.close()