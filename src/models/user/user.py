from dataclasses import dataclass


@dataclass
class User:
    userId: int
    fullName: str
    course: int
    program: str
    email: str | None
