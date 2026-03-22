from django.shortcuts import render

from django.contrib.auth import authenticate, get_user_model
from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from identity.services.token_service import issue_admin_access_token
from .serializers import AdminLoginSerializer

from .serializers import SessionPolicyUpdateSerializer,RoleScopeUpdateSerializer, SessionPolicySerializer, ApplicationSerializer, RoleSerializer, ScopeSerializer
from identity.serializers import EmployeeSerializer
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

class RoleScopeListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, app_id):
        role_scopes = RoleScope.objects.filter(application_id=app_id)

        data = [
            {
                "id": rs.id,
                "role": rs.role.name,
                "scope": rs.scope.name
            }
            for rs in role_scopes
        ]

        return Response(data)

class RoleScopeUpdateView(APIView):
    permission_classes=[IsAuthenticated]

    def put(self, request):
        application = request.data.get("application")
        role = request.data.get("role")
        scopes = request.data.get("scopes", [])

        try:
            app = Application.objects.get(client_id=application)
            role = Role.objects.get(name=role)
        except:
            return Response({"error": "Invalid data"}, status=400)

        for scope_name in scopes:
            scope = Scope.objects.get(name=scope_name)

            RoleScope.objects.get_or_create(
                application=app,
                role=role,
                scope=scope
            )

        return Response({"detail": "Scopes added successfully"})

class RoleScopeDeleteView(APIView):
    def delete(self, request, rs_id):
        try:
            role_scope = RoleScope.objects.get(id=rs_id)
            role_scope.delete()
            return Response({"detail": "Deleted"})
        except RoleScope.DoesNotExist:
            return Response({"error": "Not found"}, status=404)
        
class ApplicationAccessMatrixView(APIView):
    permission_classes=[IsAuthenticated]

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
    permission_classes=[IsAuthenticated]

    def put(self, request):
        serializer = SessionPolicyUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        policy, _ = ApplicationPolicy.objects.update_or_create(
            application=data["application"],
            defaults={"session_timeout_seconds": data["session_timeout_seconds"]}
        )

        return Response({"detail": "Session policy updated"})

class SessionPolicyListCreateView(ListCreateAPIView):    
    permission_classes=[IsAuthenticated]
    queryset = ApplicationPolicy.objects.all()    
    serializer_class = SessionPolicySerializer
    
class ApplicationListCreateView(ListCreateAPIView):    
    permission_classes=[IsAuthenticated]
    queryset = Application.objects.all()    
    serializer_class = ApplicationSerializer


class ApplicationDeleteView(APIView):
    def delete(self, request, app_id):
        try:
            app = Application.objects.get(id=app_id)
            app.delete()
            return Response({"detail": "Deleted"})
        except Application.DoesNotExist:
            return Response({"error": "Not found"}, status=404)

class RoleListCreateView(ListCreateAPIView):    
    permission_classes=[IsAuthenticated]
    queryset = Role.objects.all()    
    serializer_class = RoleSerializer

class RoleDeleteView(APIView):
    def delete(self, request, role_id):
        try:
            role = Role.objects.get(id=role_id)
            role.delete()
            return Response({"detail": "Deleted"})
        except Role.DoesNotExist:
            return Response({"error": "Not found"}, status=404)

class ScopeListCreateView(ListCreateAPIView):  
    permission_classes=[IsAuthenticated]  
    queryset = Scope.objects.all()    
    serializer_class = ScopeSerializer

class ScopeDeleteView(APIView):
    def delete(self, request, scope_id):
        try:
            scope = Scope.objects.get(id=scope_id)
            scope.delete()
            return Response({"detail": "Deleted"})
        except Scope.DoesNotExist:
            return Response({"error": "Not found"}, status=404)
        
class EmployeeListCreateView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request):
        employees = User.objects.select_related("role").all()        
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)        
        serializer.is_valid(raise_exception=True)        
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class EmployeeDetailView(APIView):
    permission_classes=[IsAuthenticated]
    def get_object(self, pk):
        return User.objects.get(pk=pk)

    def get(self, request, pk):
        serializer = EmployeeSerializer(self.get_object(pk))
        return Response(serializer.data)

    def put(self, request, pk):
        employee = self.get_object(pk)
        serializer = EmployeeSerializer(employee, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class EmployeeDeleteView(APIView):
    def delete(self, request, pk):
        employee = User.objects.get(id=pk)
        employee.delete()        
        return Response(status=status.HTTP_204_NO_CONTENT)