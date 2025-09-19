from dataclasses import dataclass

from src.models.error.error_type import ErrorType


@dataclass
class Error:
    error_type: ErrorType
    message: str
