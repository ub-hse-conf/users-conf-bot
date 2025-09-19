from dataclasses import dataclass


@dataclass
class Company:
    id: int
    name: str
    description: str
    siteUrl: str
