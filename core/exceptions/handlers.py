from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        # Standardize error response format
        response.data = {
            "error": {
                "type": exc.__class__.__name__,
                "detail": response.data.get("detail", str(exc)),
                "status_code": response.status_code,
            }
        }

    return response
