import requests
from django.shortcuts import render, redirect
from .api_client import api_request
from .decorators import api_protected
from django.http import HttpResponseRedirect
from .models import Report
import jwt
from django.core.paginator import Paginator

IAM_API_BASE = "http://127.0.0.1:8000/api"


# LOGIN
def login_view(request):

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        response = requests.post(
            f"{IAM_API_BASE}/auth/login/",
            json={
                "email": email,
                "password": password,
                "client_id": "working_hour_system",
            }
        )

        if response.status_code == 200:
            request.session["access_token"] = response.json()["access_token"]
            return redirect("submit")

        return render(request, "login.html", {"error": "Invalid credentials"})
    
    error = request.GET.get("error")
    if error == "session_expired":
        return render(request, "login.html", {
        "error": "Session expired. Please login again."
    })
    return render(request, "login.html")

def get_user_from_token(request):
    token = request.session.get("access_token")

    if not token:
        return None

    payload = jwt.decode(token, options={"verify_signature": False})

    return {
        "email": payload.get("email"),
        "name": payload.get("name")
    }

# SUBMIT
@api_protected
def submit_view(request):
    print("Submit view ",request.session.get("name"))
    if request.method == "POST":
        response = api_request(request, "POST", "/working-hours/submit/")

        # FIX: detect redirect properly
        if isinstance(response, HttpResponseRedirect):
            print("Is submit view session expired detect")
            return response

        print("Submit view response status code:", response.status_code)

        if response.status_code == 403:
            return render(request, "submit.html", {
                "error": "You do not have permission to submit."
            })
        
        user = get_user_from_token(request)
        file = request.FILES.get("file")

        if file:
            Report.objects.create(
                user_email=user["email"],
                file=file
            )

            return render(request, "submit.html", {
                "message": f"Working hours submitted by {user["name"]}"
            })

    return render(request, "submit.html")

# REPORT
@api_protected
def report_view(request):
    response = api_request(request, "GET", "/working-hours/reports/")

    if isinstance(response, HttpResponseRedirect):
        print("Is report view session expired detect")
        return response

    if response.status_code == 403:
        return render(request, "reports.html", {
            "error": "Access denied. You do not have permission."
        })
    reports = Report.objects.all().order_by('-uploaded_at')
    paginator = Paginator(reports, 5)  # 5 per page
    page_number = request.GET.get('page')
    reports = paginator.get_page(page_number)
    return render(request, "reports.html", {
        "reports": reports
    })


# LOGOUT
def logout_view(request):
    request.session.pop("access_token", None)
    return redirect("login")