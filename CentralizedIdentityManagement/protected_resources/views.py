from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from identity.models import Application, RoleScope
from identity.permission import HasScope
from identity.services.audit_service import log_event
from identity.authentication import JWTAuthentication


class ApplicationSettingsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, HasScope]
    required_scopes = ["settings.read"]

    def get(self, request):
        return Response({
            "settings": "Working hour system settings"
        })

class ApplicationAccessMatrixView(APIView):
    """
    Show role-to-scope mapping for a given application.
    """
    permission_classes = [IsAuthenticated, HasScope]
    required_scopes = ["settings.read"]

    def get(self, request, client_id):
        application = Application.objects.get(client_id=client_id)

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


class WorkingHourSubmitView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, HasScope]
    required_scopes = ["report.submit"]

    def post(self, request):
        log_event(
            action="WORKING_HOUR_SUBMITTED",
            resource="WorkingHour",
            request=request,
            user=request.user
        )
        return Response({
            "message": f"Working hours submitted by {request.user.email}"
        })


class WorkingHourReportView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, HasScope]
    required_scopes = ["report.view"]

    def get(self, request):
        print("AUTH USER:", request.user)
        print("SCOPES ON REQUEST:", getattr(request, "scopes", None))

        log_event(
            action="WORKING_HOUR_REPORT_VIEWED",
            resource="WorkingHourReport",
            request=request,
            user=request.user
        )
        return Response({
            "report": "Aggregated working hour report"
        })
