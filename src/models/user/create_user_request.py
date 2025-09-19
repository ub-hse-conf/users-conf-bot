from dataclasses import dataclass


@dataclass
class CreateUserRequest:
    course: int
    name: str
    program: str
    tgId: int
    email: str | None
