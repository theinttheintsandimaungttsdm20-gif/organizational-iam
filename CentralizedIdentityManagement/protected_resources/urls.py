from django.urls import path
from .views import (
    ApplicationSettingsView, WorkingHourSubmitView, WorkingHourReportView, ApplicationAccessMatrixView,
    LeaveApplyView, LeaveApproveView
)
urlpatterns = [
    path("settings/", ApplicationSettingsView.as_view()),
    path("working-hours/submit/", WorkingHourSubmitView.as_view()),
    path("working-hours/reports/", WorkingHourReportView.as_view()),
    path("leave/apply/", LeaveApplyView.as_view()),
    path("leave/approve/", LeaveApproveView.as_view()),
]
