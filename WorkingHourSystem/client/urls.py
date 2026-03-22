from django.urls import path
from .views import login_view, submit_view, report_view, logout_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("login/", login_view, name="login"),
    path("submit/", submit_view, name="submit"),
    path("reports/", report_view, name="reports"),
    path("logout/", logout_view, name="logout")
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
