from django.shortcuts import render
from identity.models import User, RoleScope, ApplicationPolicy, Application
from django.contrib import messages
from admin_console.models import LoginAudit
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

        if response.status_code == 200:
            data = response.json()
            request.session["access_token"] = data["access_token"]
            LoginAudit.objects.create(email=email)
            return redirect("/admin-ui/dashboard/")
        
        return render(request, "admin_ui/login.html", {
            "error": "Invalid login"
        })

    return render(request, "admin_ui/login.html")

def logout_view(request):
    messages.success(request, "Logged out successfully")
    request.session.flush()
    return redirect("/admin-ui/")

def dashboard(request):
    token = request.session.get("access_token")
    employees = IAMClient.get_employees(token)
    apps = IAMClient.get_applications(token)
    roles = IAMClient.get_roles(token)
    recent_logins = LoginAudit.objects.order_by("-login_time")[:5]
    context = {
        "recent_logins": recent_logins,
        "total_employees": len(employees.json())
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

def roles_view(request):
    token = request.session.get("access_token")
    if request.method == "POST":
        IAMClient.create_role(token, request.POST.get(
            "name"))
    response = IAMClient.get_roles(token)
    logger.info(f"STATUS:, {response.status_code}")
    if response.ok:
        data = response.json()
        if isinstance(data, dict):         
            roles = data.get("results", [])    
        else: roles = data
        print("Roles:", roles)
    else: 
        roles = []    
        print("FAILED:", response.text)
    return render(request, "admin_ui/roles.html", {"roles": roles})

def delete_app(request, app_id):
    token = request.session.get("access_token")
    print("In delete application ", app_id)
    IAMClient.delete_application(token, app_id)
    return redirect("applications")

def employees_view(request):
    token = request.session.get("access_token")
    # CREATE
    if request.method == "POST":
        IAMClient.create_employee(token, request.POST.get("name"),
                                  request.POST.get("email"), request.POST.get(
                                      "contact_number"),
                                  request.POST.get("title"),  request.POST.get(
                                      "department"),
                                  request.POST.get("join_date"), request.POST.get("role_id"))
    employee_data_resp = IAMClient.get_employees(token)
    role_data_resp = IAMClient.get_roles(token)
    logger.info(f"STATUS:, {employee_data_resp.status_code}")
    if employee_data_resp.ok:
        data = employee_data_resp.json()
        if isinstance(data, dict):         
            employees = data.get("results", [])    
        else: employees = data
    else: 
        employees = []
    if role_data_resp.ok:
        data = role_data_resp.json()
        if isinstance(data, dict):         
            roles = data.get("results", [])    
        else: roles = data
    else: 
        roles = []
    return render(request, "admin_ui/employees.html", {"employees": employees, "roles": roles})


def edit_employee(request, emp_id):
    token = request.session.get("access_token")
    if request.method == "POST":
        IAMClient.update_employee(token, emp_id, request.POST.get("name"), request.POST.get("email"), request.POST.get("contact_number"),            request.POST.get(
            "title"), request.POST.get("department"), request.POST.get("join_date"), request.POST.get("role_id"),)
        return redirect("employees")
    
    employee_data_resp = IAMClient.get_employee(token, emp_id)
    roles_data_resp = IAMClient.get_roles(token)

    print("EMP STATUS:", employee_data_resp.status_code)

    if employee_data_resp.ok:
        employee = employee_data_resp.json()
    else:
        employee = {}

    if roles_data_resp.ok:
        roles = roles_data_resp.json()
    else:
        roles = []

    return render(request, "admin_ui/edit_employee.html", {"employee": employee, "roles": roles})

def delete_employee(request, emp_id):
    token = request.session.get("access_token")
    IAMClient.delete_employee(token, emp_id)
    return redirect("employees")

def settings_view(request):
    token = request.session.get("access_token")

    applications_resp = IAMClient.get_applications(token)
    roles_resp = IAMClient.get_roles(token)
    scopes_resp = IAMClient.get_scopes(token)

    if applications_resp.ok:
        applications = applications_resp.json()
        if isinstance(applications, dict):
            applications = applications.get("results", [])
    else:
        applications = []

    if roles_resp.ok:
        roles = roles_resp.json()
        if isinstance(roles, dict):
            roles = roles.get("results", [])
    else:
        roles = []

    if scopes_resp.ok:
        scopes = scopes_resp.json()
        if isinstance(scopes, dict):
            scopes = scopes.get("results", [])
    else:
        scopes = []

    selected_app = request.GET.get("application")
    role_scopes = []

    if selected_app:
        selected_app = int(selected_app) 
        role_scopes_resp = IAMClient.get_role_scopes(token, selected_app)
        if role_scopes_resp.ok:
            role_scopes = role_scopes_resp.json()
            if isinstance(role_scopes, dict):
                role_scopes = role_scopes.get("results", [])
        else:
            role_scopes = []
    else:
        selected_app = None

    return render(request, "admin_ui/settings.html", {
        "applications": applications,
        "roles": roles,
        "scopes": scopes,
        "role_scopes": role_scopes,
        "selected_app": selected_app,
    })

def create_role_view(request):
    token = request.session.get("access_token")

    if request.method == "POST":
        name = request.POST.get("name")
        IAMClient.create_role(token, name)

    return redirect("settings")

def delete_role_view(request, role_id):
    token = request.session.get("access_token")
    IAMClient.delete_role(token, role_id)
    return redirect("settings")

def create_scope_view(request):
    token = request.session.get("access_token")

    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        IAMClient.create_scope(token, name, description)

    return redirect("settings")

def delete_scope_view(request, scope_id):
    token = request.session.get("access_token")
    IAMClient.delete_scope(token, scope_id)
    return redirect("settings")

def update_role_scopes(request):
    token = request.session.get("access_token")

    if request.method == "POST":
        app_id = request.POST.get("application")

        app = Application.objects.get(id=app_id)

        payload = {
            "application": app.client_id,
            "role": request.POST.get("role"),
            "scopes": request.POST.getlist("scopes")
        }

        IAMClient.update_role_scopes(token, payload)

        return redirect(f"/admin-ui/settings/?application={app_id}")

def delete_role_scope_view(request, rs_id):
    token = request.session.get("access_token")
    application = request.GET.get("application")

    IAMClient.delete_role_scope(token, rs_id)

    return redirect(f"/admin-ui/settings/?application={application}")

def session_view(request):
    token = request.session.get("access_token")
    applications = IAMClient.get_applications(token).json()
    selected_app = request.GET.get("application")
    policies = IAMClient.get_app_session_policy(token).json()
    print("In policy p 1", policies)
    selected_policy = None
    # application_id
    application_id = None
    app_map = {app["id"]:app["name"] for app in applications}
    for app in applications:
        if app.get("client_id") == selected_app:
            application_id = app.get("id")
            break
    # policy with application id
    for p in policies:
        print("In policy p 2", p)
        p["application_name"] = app_map.get(p.get("application"), "Unknown app")
        print("Name of applications ",p["application_name"])
        if p.get("application") == application_id:
            selected_policy = p.get("session_timeout_seconds")

    return render(request, "admin_ui/session.html", {
        "applications": applications,
        "policies": policies,
        "selected_app": selected_app,
        "selected_policy": selected_policy
    })

def update_session_policy_ui(request):
    token = request.session.get("access_token")
    if request.method == "POST":
        application = request.POST.get("application")
        timeout = int(request.POST.get("timeout"))
        response = IAMClient.update_session_policy(token, application, timeout)

        if response.status_code == 200:
            messages.success(request, "Session policy updated successfully")
        else:
            messages.error(request, "Failed to update session policy")

        return redirect(f"/admin-ui/session/?application={application}")