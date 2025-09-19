from src.models import Error


class ServerErrorException(RuntimeError):
    def __init__(self, message: str, error: Error):
        self.message = message
        self.error = error

    def __str__(self):
        return f"{self.message}, error: {self.error.message}, type: {self.error.error_type.name}"