from django.shortcuts import render
from identity.models import User, RoleScope, ApplicationPolicy

from django.shortcuts import render, redirect
from .services import IAMClient
import logging

logger = logging.getLogger(__name__)


def admin_login(request):
    if request.method == "POST":

        email = request.POST.get("email").strip()
        password = request.POST.get("password").strip()

        response = IAMClient.login(email, password)
        print(response.json)
        logger.error(f"STATUS:, {response.status_code}")
        logger.error(f"BODY:, {response.text}")
        if response.status_code == 200:

            data = response.json()

            request.session["access_token"] = data["access_token"]

            return redirect("/admin-ui/dashboard/")

        return render(request, "admin_ui/login.html", {
            "error": "Invalid login"
        })

    return render(request, "admin_ui/login.html")


def dashboard(request):
    token = request.session.get("access_token")
    employees = IAMClient.get_employees(token)
    apps = IAMClient.get_applications(token)
    roles = IAMClient.get_roles(token)
    context = {"total_employees": len(employees.json())
               if employees.ok else 0, 
               "total_apps": len(apps.json())
               if apps.ok else 0, 
               "total_roles": len(roles.json())
               if roles.ok else 0}
    return render(request, "admin_ui/dashboard.html", context)


def applications_view(request):
    token = request.session.get("access_token")
    if request.method == "POST":
        IAMClient.create_application(token, request.POST.get(
            "name"), request.POST.get("client_id"))
    response = IAMClient.get_applications(token)
    logger.info(f"STATUS:, {response.status_code}")
    if response.ok:
        data = response.json()
        if isinstance(data, dict):         
            applications = data.get("results", [])    
        else: applications = data
        print("APPS:", applications)
    else: 
        applications = []    
        print("FAILED:", response.text)
    return render(request, "admin_ui/applications.html", {"applications": applications})

def delete_app(request, app_id):
    token = request.session.get("access_token")
    IAMClient.delete_application(token, app_id)
    return redirect("applications")

def users_view(request):
    users = User.objects.all()
    return render(request, "admin_ui/users.html", {"users": users})


def rolescope_view(request):
    scopes = RoleScope.objects.all()
    return render(request, "admin_ui/rolescope.html", {"scopes": scopes})


def session_view(request):
    policies = ApplicationPolicy.objects.all()
    return render(request, "admin_ui/session.html", {"policies": policies})
