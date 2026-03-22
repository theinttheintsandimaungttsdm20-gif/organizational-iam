import requests
from django.shortcuts import redirect

IAM_API_BASE = "http://127.0.0.1:8000/api"

def api_request(request, method, url, **kwargs):
    token = request.session.get("access_token")

    headers = kwargs.pop("headers", {})
    headers["Authorization"] = f"Bearer {token}"

    response = requests.request(
        method,
        f"{IAM_API_BASE}{url}",
        headers=headers,
        **kwargs
    )

    # HANDLE TOKEN EXPIRED
    if response.status_code == 401:
        request.session.pop("access_token", None)
        print("Session expired redirected to login")
        return redirect("/login/?error=session_expired")
    return response