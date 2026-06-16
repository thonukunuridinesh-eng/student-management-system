from http import HTTPStatus

from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is None:
        return None

    message = HTTPStatus(response.status_code).phrase

    if response.status_code == 400:
        message = "Validation error"
    elif response.status_code == 401:
        message = "Authentication failed"
    elif response.status_code == 403:
        message = "Permission denied"
    elif response.status_code == 404:
        message = "Resource not found"

    response.data = {
        "success": False,
        "status_code": response.status_code,
        "message": message,
        "errors": response.data,
    }
    return response
