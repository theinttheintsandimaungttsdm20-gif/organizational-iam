from django.urls import path
from identity.views import UserLoginView

urlpatterns = [
    path("auth/login/", UserLoginView.as_view(), name="user-login"),
]
