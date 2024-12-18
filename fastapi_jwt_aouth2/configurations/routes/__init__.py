from fastapi_jwt_aouth2.configurations.routes.routes import Routes
from fastapi_jwt_aouth2.internal.routes import health
from fastapi_jwt_aouth2.internal.routes.auth import auth

__routes__ = Routes(routers=(health.router, auth.router))
