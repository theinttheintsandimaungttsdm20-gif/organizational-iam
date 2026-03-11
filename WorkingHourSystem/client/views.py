import requests
from django.shortcuts import render

from django.shortcuts import render, redirect

IAM_API_BASE = "http://127.0.0.1:8000/api"


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

    return render(request, "login.html")


def submit_view(request):
    token = request.session.get("access_token")
    if not token:
        return redirect("login")

    if request.method == "POST":
        response = requests.post(
            f"{IAM_API_BASE}/working-hours/submit/",
            headers={"Authorization": f"Bearer {token}"}
        )

        if response.status_code == 401:
            request.session.flush()
            return redirect("login")

        return render(request, "submit.html", {
            "message": response.json()
        })

    return render(request, "submit.html")


def report_view(request):
    token = request.session.get("access_token")
    if not token:
        return redirect("login")

    response = requests.get(
        f"{IAM_API_BASE}/working-hours/reports/",
        headers={"Authorization": f"Bearer {token}"}
    )

    if response.status_code == 403:
        return render(request, "reports.html", {
            "error": "Access denied. You don't have permission to view this reports."
        })

    if response.status_code == 401:
        request.session.flush()
        return redirect("login")

    return render(request, "reports.html", {
        "data": response.json()
    })


def logout_view(request):
    request.session.flush()
    return redirect("login")
