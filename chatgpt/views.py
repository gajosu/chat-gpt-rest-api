"""
Views
"""

from typing import Optional

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from revChatGPT.V1 import Chatbot


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


def get_access_token(request: HttpRequest) -> str:
    """
    Returns the access token from the request.
    """
    return request.headers.get("Authorization")


@require_http_methods(["POST"])
def start_new_conversation(request: HttpRequest) -> JsonResponse:
    """
    Starts a new conversation given the prompt.
    """

    access_token = get_access_token(request)
    prompt: Optional[str] = request.POST.get("prompt", None)
    title = request.POST.get("title", None)
    model: str = request.POST.get("model", "")
    autocontinue: bool = request.POST.get("autocontinue", "false").lower() == "true"

    error_response = validate_prompt(prompt)
    if error_response:
        return error_response

    chatbot = get_chatbot(access_token)
    parts = list(chatbot.ask(
        prompt=prompt,
        model=model,
        autocontinue=autocontinue
    ))

    data = parts[-1]

    if title is not None:
        chatbot.change_title(data["conversation_id"], title)

    return JsonResponse({
        "response": data
    }, safe=False)


@require_http_methods(["GET"])
def get_conversations(request: HttpRequest) -> HttpResponse:
    """
    Gets all conversations.
    """
    access_token = get_access_token(request)
    limit: int = int(request.GET.get("limit", 10))
    offset: int = int(request.GET.get("offset", 0))

    chatbot = get_chatbot(access_token)
    conversations = chatbot.get_conversations(
        limit=limit,
        offset=offset
    )

    return JsonResponse(conversations, safe=False)


@require_http_methods(["GET"])
def get_messages(request: HttpRequest, conversation_id: str) -> HttpResponse:
    """
    Gets all conversations.
    """
    access_token = get_access_token(request)

    chatbot = get_chatbot(access_token)
    conversations = chatbot.get_msg_history(
        convo_id=conversation_id,
    )

    return JsonResponse(conversations, safe=False)


@require_http_methods(["POST"])
def ask(request: HttpRequest, conversation_id: str) -> JsonResponse:
    """
    Asks the chatbot for a response given the prompt and conversation_id.
    """
    access_token = get_access_token(request)
    prompt: Optional[str] = request.POST.get("prompt", None)
    parent_id: str = request.POST.get("parent_id", "")
    model: str = request.POST.get("model", "")
    autocontinue: bool = request.POST.get("autocontinue", "false").lower() == "true"

    error_response = validate_prompt(prompt)
    if error_response:
        return error_response

    chatbot = get_chatbot(access_token)

    parts = list(chatbot.ask(
        prompt=prompt,
        conversation_id=conversation_id,
        parent_id=parent_id,
        model=model,
        autocontinue=autocontinue
    ))

    data = parts[-1]

    return JsonResponse({
        "response": data
    }, safe=False)


@require_http_methods(["DELETE"])
def delete_conversation(request: HttpRequest, conversation_id: str) -> HttpResponse:
    """
    Deletes the conversation with the given conversation_id.
    """
    access_token = get_access_token(request)

    chatbot = get_chatbot(access_token)
    chatbot.delete_conversation(conversation_id)

    # Empty response
    return HttpResponse(status=204)


@require_http_methods(["DELETE"])
def delete_all_conversations(request: HttpRequest) -> HttpResponse:
    """
    Deletes all conversations.
    """
    access_token = get_access_token(request)

    chatbot = get_chatbot(access_token)
    chatbot.clear_conversations()

    return HttpResponse(status=204)
