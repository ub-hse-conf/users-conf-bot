from dataclasses import dataclass


@dataclass
class Vote:
    userId: int
    answer: str
    id: int
    eventId: int
