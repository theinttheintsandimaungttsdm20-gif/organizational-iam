from django.urls import path
from .views import ApplicationSettingsView,WorkingHourSubmitView, WorkingHourReportView, ApplicationAccessMatrixView

urlpatterns = [
    path("settings/", ApplicationSettingsView.as_view()),
    path("working-hours/submit/", WorkingHourSubmitView.as_view()),
    path("working-hours/reports/", WorkingHourReportView.as_view()),
]
