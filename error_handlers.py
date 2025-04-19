from functools import wraps
from flask import render_template

class ErrorCodes:
    USER_NOT_FOUND = 100
    INVALID_PASSWORD = 150
    USER_EXISTS = 200
    REGISTER_SUCCESS = 250
    INTERNAL_ERROR = 500
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    TIMEOUT = 408
    BAD_REQUEST = 410
    RESOURCE_EXHAUSTED = 504

def handle_error(code, message=None):
    def decorator(function):
        @wraps(function)
        def wrapper(error):
            return render_template("response.html", 
                                 code=code,
                                 default_message=message or str(error))
        return wrapper
    return decorator
