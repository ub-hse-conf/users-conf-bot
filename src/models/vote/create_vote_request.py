from dataclasses import dataclass


@dataclass
class CreateVoteRequest:
    userTgId: int
    answer: str
