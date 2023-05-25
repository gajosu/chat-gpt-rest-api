from django.http import JsonResponse
from typing import Optional


class AccessTokenMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request) -> Optional[JsonResponse]:
        access_token: Optional[str] = request.headers.get(
            "Authorization", None)
        if access_token is None:
            # json response
            return JsonResponse({
                "error": "access_token is required"
            }, status=401)

        return self.get_response(request)
