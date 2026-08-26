import time
from django.http import HttpResponseForbidden

class LogRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        #process before
        print(f"[Middleware] Request Path: {request.path}")
        response = self.get_response(request)

        #process after
        print(f"[Middleware] Response Status: {response.status_code}")
        return response

class ResponseTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        #process before
        start_time = time.time()
        response = self.get_response(request)
        duration = time.time() - start_time
        print(f"[Middleware] Request Time: {duration:.2f} seconds")
        return response

class BlockIPMiddleware:
    BLOCKED_IPS = []
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        ip = request.META.get('REMOTE_ADDR')
        if ip in self.BLOCKED_IPS:
            return HttpResponseForbidden("You have been blocked by your IP address")
        response = self.get_response(request)
        return response