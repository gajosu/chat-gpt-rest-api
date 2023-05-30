"""chatgpt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from chatgpt.views import (
    start_new_conversation,
    get_conversations,
    delete_all_conversations,
    delete_conversation,
    ask,
    get_messages
)

urlpatterns = [
    path('conversations', get_conversations, name="get_conversations"),
    path('conversations/new', start_new_conversation, name="start_new_conversation"),
    path('conversations/all', delete_all_conversations , name="delete_all_conversation"),
    path('conversations/<str:conversation_id>', delete_conversation , name="delete_conversation"),
    path('conversations/<str:conversation_id>/ask', ask , name="ask"),
    path('conversations/<str:conversation_id>/messages', get_messages, name="get_messages"),
]
