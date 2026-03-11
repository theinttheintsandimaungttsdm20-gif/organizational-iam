from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None and response.status_code == 403:
        return Response(
            {"detail": "You do not have permission to perform this action"},
            status=status.HTTP_403_FORBIDDEN
        )

    return response
