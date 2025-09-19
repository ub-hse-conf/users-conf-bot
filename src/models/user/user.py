from dataclasses import dataclass


@dataclass
class User:
    userId: int
    name: str
    course: int
    program: str
    email: str | None
