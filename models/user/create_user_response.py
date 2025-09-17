from dataclasses import dataclass

from models.user.user import User


@dataclass
class CreateUserResponse:
    user: User
