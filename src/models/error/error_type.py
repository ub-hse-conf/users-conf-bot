import enum


class ErrorType(enum.Enum):
    NONE = 0
    USER_NOT_FOUND = 1
    VISIT_ALREADY_EXISTS = 2

    def __missing__(self, key):
        return self.NONE
