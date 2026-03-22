from django.shortcuts import redirect
from django.contrib import messages
import jwt
import time

class JWTSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.path == "/admin-ui/":
            return self.get_response(request)

        token = request.session.get("access_token")

        # no session → go back to /admin-ui/
        if not token:
            messages.warning(request, "Session expired. Please login again.")
            if request.path.startswith("/admin-ui/"):
                messages.warning(request, "Session expired. Please login again.")
                return redirect("/admin-ui/")
            return self.get_response(request)

        # check JWT expiry
        try:
            payload = jwt.decode(token, options={"verify_signature": False})

            if payload.get("exp") < time.time():
                print("Expiry Token ")
                messages.warning(request, "Session expired. Please login again.")
                request.session.flush()
                return redirect("/admin-ui/")

        except Exception:
            print("Exception Token ")
            messages.warning(request, "Session expired. Please login again.")
            request.session.flush()
            return redirect("/admin-ui/")

        return self.get_response(request)