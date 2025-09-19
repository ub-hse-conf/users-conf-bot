__all__ = [
    "health"
]

from aiohttp.web import Application

from src.api.endpoint.health import health

def register_endpoints(app: Application):
    app.router.add_get("/health", health)