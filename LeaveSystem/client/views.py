from django.shortcuts import get_object_or_404, render, redirect
from .api_client import api_request
from .decorators import api_protected
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
import requests
import jwt
from .models import Leave
from django.core.paginator import Paginator

IAM_API_BASE = "http://127.0.0.1:8000/api"


def get_user_from_token(request):
    token = request.session.get("access_token")

    if not token:
        return None

    payload = jwt.decode(token, options={"verify_signature": False})

    return {
        "email": payload.get("email"),
        "name": payload.get("name"),
        "role": payload.get("role"),
        "scopes": payload.get("scope", [])
    }


def login_view(request):
    error = request.GET.get("error")
    print("Login error ",error)
    if error == "session_expired":
        return render(request, "login.html", {
            "error": "Session expired. Please login again."
        })
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        response = requests.post(
            f"{IAM_API_BASE}/auth/login/",
            json={
                "email": email,
                "password": password,
                "client_id": "leave_application",
            }
        )

        if response.status_code == 200:
            request.session["access_token"] = response.json()["access_token"]
            return redirect("apply_leave")

        return render(request, "login.html", {"error": "Invalid credentials"})
    return render(request, "login.html")


@api_protected
def apply_leave_view(request):
    user = get_user_from_token(request)
    if request.method == "POST":
        response = api_request(request, "POST", "/leave/apply/")
        print("apply_leave_view Response status : ", response.status_code)

        if isinstance(response, HttpResponseRedirect):
            print("Is submit view session expired detect")
            return response
        
        if response.status_code == 403:
            return render(request, "apply_leave.html", {
                "error": "You do not have permission to apply Leave."
            })
        Leave.objects.create(
            user_email=user["email"],
            user_name=user["name"],
            start_date=request.POST.get("start_date"),
            end_date=request.POST.get("end_date"),
            reason=request.POST.get("reason"),
            status="PENDING"
        )

        return render(request, "apply_leave.html", {
            "message": f"Leave submitted by {user['email']}",
            "user": user
        })

    return render(request, "apply_leave.html", {"user": user})


@api_protected
def leave_list_view(request):
    user = get_user_from_token(request)
    scopes = user.get("scopes", []) if user else []

    if "leave.approve" in scopes:
        # Manager / Approver → see all
        leaves = Leave.objects.all().order_by('-created_at')
    else:
        # Normal user → see only own
        leaves = Leave.objects.filter(
            user_email=user["email"]
        ).order_by('-created_at')
    paginator = Paginator(leaves, 5)
    page_number = request.GET.get("page")
    leaves = paginator.get_page(page_number)

    return render(request, "leave_list.html", {
        "leaves": leaves,
        "user": user,
        "scopes": user.get("scopes", []) if user else []
    })


@api_protected
def approve_leave_view(request):
    user = get_user_from_token(request)
    leave_id = request.POST.get("id")
    action = request.POST.get("action")  # approve / reject
    print("--- action is ---", action)
    if action not in ["approve", "reject"]:
        print("--- action is not in approve or reject ---")
        return redirect("leave_list")

    print("--- action ---")
    response = api_request(request, "POST", "/leave/approve/",
                           data={"action": action}
                           )
    print("Approve leave response status code ", response.status_code)

    if isinstance(response, HttpResponseRedirect):
            print("Is submit view session expired detect")
            return response
    
    if response.status_code == 403:
        return redirect("/leave_list/?error=permission_denied")

    leave = get_object_or_404(Leave, id=leave_id)

    if action == "approve":
        leave.status = "APPROVED"
    else:
        leave.status = "REJECTED"

    leave.approved_by = user["email"]
    leave.save()

    return redirect("leave_list")


def logout_view(request):
    request.session.pop("access_token", None)
    request.session.pop("user", None)
    return redirect("login")
