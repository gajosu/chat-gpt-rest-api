from revChatGPT.typings import Error as ChatbotError
from django.http import JsonResponse
from typing import Optional
import json


class ErrorHandlerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception) -> Optional[JsonResponse]:    
        if isinstance(exception, ChatbotError):
            # parse exception.message json and return it
            jsonMessage = json.loads(exception.message)

            return JsonResponse({
                # "error": jsonMessage
                "error": jsonMessage
            }, status=500)
