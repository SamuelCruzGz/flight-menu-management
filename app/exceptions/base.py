class ApplicationException(Exception):
    """
    Base class for all business exceptions.
    """

    default_message = "An application error occurred."

    def __init__(self, message: str | None = None):
        super().__init__(message or self.default_message)


class ValidationException(ApplicationException):
    """
    Raised when business validation fails.
    """

    default_message = "Validation failed."


class NotFoundException(ApplicationException):
    """
    Raised when a requested resource cannot be found.
    """

    default_message = "Resource not found."


class ConflictException(ApplicationException):
    """
    Raised when a business conflict occurs.
    """

    default_message = "Resource conflict."