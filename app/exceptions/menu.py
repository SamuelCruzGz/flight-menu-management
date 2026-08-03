from app.exceptions.base import (
    ConflictException,
    NotFoundException,
)


class FlightNotFoundException(NotFoundException):
    default_message = (
        "The specified flight does not exist."
    )


class MenuNotFoundException(NotFoundException):
    default_message = (
        "The requested menu was not found."
    )


class DuplicateMenuException(ConflictException):
    default_message = (
        "A menu already exists for the specified flight and date range."
    )


class DuplicateDishException(ConflictException):
    default_message = (
        "Duplicated dishes are not allowed within the same menu."
    )
    
class DuplicateMenuException(
    ConflictException,
):
    default_message = (
        "A menu already exists for the specified flight and date range."
    )