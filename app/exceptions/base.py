class BusinessException(Exception):
    """
    Base class for all business exceptions.
    """

    status_code = 500

    default_message = "An application error occurred."

    def __init__(
        self,
        message: str | None = None,
    ):
        self.message = (
            message
            or self.default_message
        )


class ValidationException(BusinessException):
    """
    Raised when business validation fails.
    """

    status_code = 400

    default_message = "Validation failed."


class NotFoundException(BusinessException):
    """
    Raised when a requested resource cannot be found.
    """

    status_code = 404

    default_message = "Resource not found."


class ConflictException(BusinessException):
    """
    Raised when a business conflict occurs.
    """

    status_code = 409

    default_message = "Resource conflict."