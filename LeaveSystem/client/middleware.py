from django.shortcuts import redirect

class ClientSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.path.startswith("/login"):
            return self.get_response(request)

        token = request.session.get("access_token")

        if not token:
            print("Middleware Token Expired!!")
            return redirect("login")

        return self.get_response(request)