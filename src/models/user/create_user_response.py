from dataclasses import dataclass

from src.models.user.user import User


@dataclass
class CreateUserResponse:
    user: User
