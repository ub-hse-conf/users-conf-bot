from dataclasses import dataclass

from models.error.error_type import ErrorType


@dataclass
class Error:
    error_type: ErrorType
    message: str
