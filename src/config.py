from decouple import config

from src.models import WorkingMode

BASE_URL = config("BASE_URL")

REDIS_HOST = config("REDIS_HOST", default="localhost")
REDIS_PORT = config("REDIS_PORT", default="6379")

REDIS_TTL: int = config("REDIS_TTL", cast=int)

USERNAME_API = config("USERNAME_API")
PASSWORD_API = config("PASSWORD_API")

DEBUG: bool = config("DEBUG", cast=bool, default=False)
IS_PROD: bool = not DEBUG

BOT_TOKEN = config("BOT_TOKEN")

WORKING_MODE = config("WORKING_MODE", cast=WorkingMode)

WEBHOOK_URL = config("WEBHOOK_URL", default=None)
WEBHOOK_PATH = config("WEBHOOK_PATH", default="/")