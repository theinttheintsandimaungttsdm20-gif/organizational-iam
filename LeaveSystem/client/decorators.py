from functools import wraps
from django.shortcuts import redirect

def api_protected(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        token = request.session.get("access_token")

        if not token:
            return redirect("login")

        return view_func(request, *args, **kwargs)

    return wrapper