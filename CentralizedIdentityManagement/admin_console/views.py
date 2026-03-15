from django.shortcuts import render

from django.contrib.auth import authenticate, get_user_model
from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from identity.services.token_service import issue_admin_access_token
from .serializers import AdminLoginSerializer
from .serializers import SessionPolicyUpdateSerializer,RoleScopeUpdateSerializer, UserCreateSerializer, ApplicationSerializer
from identity.permission import HasScope
from identity.models import User, Role,Scope, Application, ApplicationPolicy, RoleScope

User = get_user_model()


class AdminLoginView(APIView):
    permission_classes = []  # allow login without token

    def post(self, request):
        serializer = AdminLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        user = authenticate(request, email=email, password=password)
        if not user:
            return Response(
                {"detail": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        token = issue_admin_access_token(user)

        return Response({
            "access_token": token,
            "token_type": "Bearer",
        })

class EmployeeListCreateView(APIView):
    permission_classes = [HasScope]
    required_scopes = ["settings.write"]

    def get(self, request):
        users = User.objects.all().values("id", "email", "role__name")
        return Response(users)

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class EmployeeRoleUpdateView(APIView):
    permission_classes = [HasScope]
    required_scopes = ["settings.write"]

    def put(self, request, user_id):
        from .serializers import UserRoleUpdateSerializer
        serializer = UserRoleUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = User.objects.get(id=user_id)
            role = Role.objects.get(id=serializer.validated_data["role_id"])
        except (User.DoesNotExist, Role.DoesNotExist):
            return Response({"detail": "User or Role not found"}, status=404)

        user.role = role
        user.save()
        return Response({"detail": "Role updated"})

class RoleScopeUpdateView(APIView):
    permission_classes = [HasScope]
    required_scopes = ["settings.write"]

    def put(self, request):
        serializer = RoleScopeUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        application = serializer.validated_data["application"]
        role = serializer.validated_data["role"]
        scopes = serializer.validated_data["scopes"]

        RoleScope.objects.filter(role=role).delete()

        for scope_name in scopes:
            scope, _ = Scope.objects.get_or_create(name=scope_name)
            RoleScope.objects.create(role=role, scope=scope, application=application)

        return Response({"detail": "Scopes updated"})

class ApplicationAccessMatrixView(APIView):
    permission_classes = [HasScope]
    required_scopes = ["settings.read"]

    def get(self, request, client_id):
        application = get_object_or_404(
            Application, client_id=client_id
        )

        role_scopes = (
            RoleScope.objects
            .filter(application=application)
            .select_related("role", "scope")
        )

        matrix = {}
        for rs in role_scopes:
            matrix.setdefault(rs.role.name, []).append(rs.scope.name)

        return Response({
            "application": application.client_id,
            "access_matrix": [
                {"role": role, "scopes": scopes}
                for role, scopes in matrix.items()
            ]
        })

class SessionPolicyUpdateView(APIView):
    permission_classes = [HasScope]
    required_scopes = ["settings.write"]

    def put(self, request):
        serializer = SessionPolicyUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        policy, _ = ApplicationPolicy.objects.update_or_create(
            application=data["application"],
            defaults={"session_timeout_seconds": data["session_timeout_seconds"]}
        )

        return Response({"detail": "Session policy updated"})
    
class ApplicationListCreateView(ListCreateAPIView):    
    queryset = Application.objects.all()    
    serializer_class = ApplicationSerializer