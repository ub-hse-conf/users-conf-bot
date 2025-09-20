from dataclasses import dataclass

from src.models.user.user_role import UserRole


@dataclass
class User:
    userId: int
    fullName: str
    course: int
    program: str
    role: UserRole
    email: str | None
