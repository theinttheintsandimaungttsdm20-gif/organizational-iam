from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from identity.serializers import UserLoginSerializer
from identity.services.token_service import issue_access_token

class UserLoginView(APIView):
    """
    Normal user login for client applications
    (e.g. working_hour_system, leave_system)
    """
    permission_classes = []  # allow login without token

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]
        client_id = serializer.validated_data["client_id"]

        user = authenticate(request, email=email, password=password)
        if not user:
            return Response(
                {"detail": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        token = issue_access_token(user, client_id)

        return Response({
            "access_token": token,
            "token_type": "Bearer"
        })
