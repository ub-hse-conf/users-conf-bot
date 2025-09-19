from dataclasses import dataclass


@dataclass
class Visitable:
    id: int
    name: str
    description: str
