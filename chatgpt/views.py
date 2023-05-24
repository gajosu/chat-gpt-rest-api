from django.http import HttpRequest, JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from OpenAIAuth import Error as AuthError
from revChatGPT.V1 import Chatbot
from typing import Optional

def validate_access_token(access_token: Optional[str]) -> Optional[JsonResponse]:
    """
    Validates the access_token and returns a JsonResponse if it is invalid.
    Otherwise, returns None.
    """
    if access_token is None:
        # 401 Unauthorized
        return JsonResponse({
            "error": "access_token is required"
        }, status=401)
    return None

def validate_prompt(prompt: Optional[str]) -> Optional[JsonResponse]:
    """
    Validates the prompt and returns a JsonResponse if it is invalid.
    Otherwise, returns None.
    """
    if prompt is None:
        # 400 Bad Request
        return JsonResponse({
            "error": "prompt is required"
        }, status=400)
    return None

def get_chatbot(access_token: str) -> Chatbot:
    """
    Returns a Chatbot instance with the given access_token.
    """
    return Chatbot(config={
        "access_token": access_token
    })
    
def open_ai_error_response(error: AuthError) -> JsonResponse:
    """
    Returns a JsonResponse with the given AuthError.
    """
    return JsonResponse({
        "error": {
            "location": error.location,
            "status_code": error.status_code,
            "details": error.details
        }
    }, status=500)

@require_http_methods(["PUT"])
def start_new_conversation(request: HttpRequest) -> JsonResponse:
    """
    Starts a new conversation given the prompt.
    """
    access_token: Optional[str] = request.headers.get("Authorization", None)
    prompt: Optional[str] = request.POST.get("prompt", None)

    error_response: Optional[JsonResponse] = validate_access_token(access_token)
    if error_response:
        return error_response

    error_response = validate_prompt(prompt)
    if error_response:
        return error_response

    chatbot = get_chatbot(access_token)

    try:
        for data in chatbot.ask(prompt):
            pass

        return JsonResponse({
            "response": data
        }, safe=False)
    except AuthError as error:
        return open_ai_error_response(error)

@require_http_methods(["DELETE"])
def get_conversations(request: HttpRequest) -> HttpResponse:
    """
    Gets all conversations.
    """
    access_token: Optional[str] = request.headers.get("Authorization", None)

    error_response: Optional[JsonResponse] = validate_access_token(access_token)
    if error_response:
        return error_response

    try:
        chatbot = get_chatbot(access_token)
        conversations = chatbot.get_conversations()
        
        return JsonResponse({
            "conversations": conversations
        }, safe=False)
    
    except AuthError as error:
        return open_ai_error_response(error)
    
@require_http_methods(["POST"])
def ask(request: HttpRequest, conversation_id: str) -> JsonResponse:
    """
    Asks the chatbot for a response given the prompt and conversation_id.
    """
    access_token: Optional[str] = request.headers.get("Authorization", None)
    prompt: Optional[str] = request.POST.get("prompt", None)

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
    except AuthError as error:
        return open_ai_error_response(error)


@require_http_methods(["DELETE"])
def delete_conversation(request: HttpRequest, conversation_id: str) -> HttpResponse:
    """
    Deletes the conversation with the given conversation_id.
    """
    access_token: Optional[str] = request.headers.get("Authorization", None)

    error_response: Optional[JsonResponse] = validate_access_token(access_token)
    if error_response:
        return error_response

    try:
        chatbot = get_chatbot(access_token)
        chatbot.delete_conversation(conversation_id)
        
        # Empty response
        return HttpResponse(status=204)
    
    except AuthError as error:
        return open_ai_error_response(error)
    
    
@require_http_methods(["DELETE"])
def delete_all_conversations(request: HttpRequest) -> HttpResponse:
    """
    Deletes all conversations.
    """
    access_token: Optional[str] = request.headers.get("Authorization", None)

    error_response: Optional[JsonResponse] = validate_access_token(access_token)
    if error_response:
        return error_response

    try:
        chatbot = get_chatbot(access_token)
        chatbot.clear_conversations()
        
        # Empty response
        return HttpResponse(status=204)
    
    except AuthError as error:
        return open_ai_error_response(error)

