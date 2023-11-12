from core.exceptions.base import CustomException


class IncorrectPasswordException(CustomException):
    status_code = 400
    error_code = "AUTH__INCORRECT_PASSWORD"
    message = "credentials were incorrect"
