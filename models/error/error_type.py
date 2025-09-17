import enum


class ErrorType(enum.Enum):
    NONE = 0

    def __missing__(self, key):
        return self.NONE
