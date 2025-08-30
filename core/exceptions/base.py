from rest_framework.exceptions import APIException


class DomainException(APIException):
    """Base class for domain-specific exceptions."""
    status_code = 400
    default_detail = "A server error occurred."
    default_code = "domain_error"
