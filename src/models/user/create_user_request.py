from dataclasses import dataclass


@dataclass
class CreateUserRequest:
    course: int
    fullName: str
    program: str
    tgId: int
    email: str | None
