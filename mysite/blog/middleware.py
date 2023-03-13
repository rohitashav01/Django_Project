from django.conf import settings

class CustomMiddleware:
    if settings.DEBUG:
        def __init__(self, get_response):
            self.get_response = get_response

        def __call__(self, request):
            #print("custom middleware before next middleware/view")
            
            response = self.get_response(request)

            #print("custom middleware after response or previous middleware")
            return response