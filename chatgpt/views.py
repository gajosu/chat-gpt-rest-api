from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_http_methods
from revChatGPT.V1 import Chatbot

@require_http_methods(["POST"])
def ask(request: HttpRequest):
    access_token = request.headers.get("Authorization", None)
    prompt = request.POST.get("prompt", None)
    conversation_id = request.GET.get("conversation_id", "")

    if access_token is None:
        # 401 Unauthorized
        return JsonResponse({
                "error": "access_token is required"
            },
            status=401
        )

    if prompt is None:
        # 400 Bad Request
        return JsonResponse({
                "error": "prompt is required"
            },
            status=400
        )
    

    chatbot = Chatbot(config={
        "access_token": access_token
    })

    try:
        print("Chatbot: ")
        prev_text = ""
        for data in chatbot.ask(
            prompt,
            conversation_id
        ):
            message = data["message"][len(prev_text) :]
            print(message, end="", flush=True)
            prev_text = data["message"]
        
        return JsonResponse({
                "response": data
            },
            safe=False
        )
    except Exception as e:
        return JsonResponse({
                "error": str(e)
            },
            status=500
        )
    
