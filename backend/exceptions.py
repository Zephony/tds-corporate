class InvalidRequestData(Exception):
    """
    The request data was syntactically or semantically invalid. This exception
    is usually raised from the actions or the models layer. This exception is
    not to be confused with the custom exceptions of Voluptuous which is used
    to validate the schema of the request data rather than the actual value of
    the data being sent.
    """

    def __init__(self, errors=None, message=None, http_status=422):
        """
        :param list(dict) errors: Each dict has keys `field` & `description`
        """

        self.errors = errors[:] if errors else []
        self.message = message
        self.http_status = http_status

class Unauthorized(Exception):
    def __init__(self, message=None, http_status=401):
        self.message = message
        self.http_status = http_status

class Forbidden(Exception):
    def __init__(self, message=None, http_status=403):
        self.message = message
        self.http_status = http_status

class ResourceNotFound(Exception):
    def __init__(self, message=None, http_status=404):
        self.message = message
        self.http_status = http_status

class InternalServerError(Exception):
    def __init__(self, message=None, http_status=500):
        self.message = message
        self.http_status = http_status

