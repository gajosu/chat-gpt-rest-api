from django.http import HttpRequest, JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from revChatGPT.V1 import Chatbot
from typing import Optional

def validate_access_token(access_token: Optional[str]) -> Optional[JsonResponse]:
    if access_token is None:
        # 401 Unauthorized
        return JsonResponse({
            "error": "access_token is required"
        }, status=401)
    return None

def validate_prompt(prompt: Optional[str]) -> Optional[JsonResponse]:
    if prompt is None:
        # 400 Bad Request
        return JsonResponse({
            "error": "prompt is required"
        }, status=400)
    return None

def get_chatbot(access_token: str) -> Chatbot:
    return Chatbot(config={
        "access_token": access_token
    })

@require_http_methods(["POST"])
def ask(request: HttpRequest) -> JsonResponse:
    access_token: Optional[str] = request.headers.get("Authorization", None)
    prompt: Optional[str] = request.POST.get("prompt", None)
    conversation_id: str = request.GET.get("conversation_id", "")

    error_response: Optional[JsonResponse] = validate_access_token(access_token)
    if error_response:
        return error_response

    error_response = validate_prompt(prompt)
    if error_response:
        return error_response

    chatbot = get_chatbot(access_token)

    try:
        for data in chatbot.ask(prompt, conversation_id):
            pass

        return JsonResponse({
            "response": data
        }, safe=False)
    except Exception as e:
        return JsonResponse({
            "error": str(e)
        }, status=500)

@require_http_methods(["DELETE"])
def delete_conversation(request: HttpRequest, conversation_id: str) -> HttpResponse:
    access_token: Optional[str] = request.headers.get("Authorization", None)

    error_response: Optional[JsonResponse] = validate_access_token(access_token)
    if error_response:
        return error_response

    try:
        chatbot = get_chatbot(access_token)
        chatbot.delete_conversation(conversation_id)
        
        # Empty response
        return HttpResponse(status=204)
    
    except Exception as e:
        return JsonResponse({
            "error": str(e)
        }, status=500)

