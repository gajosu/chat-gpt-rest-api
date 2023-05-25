import json
from unittest import mock

from django.test import Client, RequestFactory, TestCase
from revChatGPT.V1 import Chatbot


class TestMessagesView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @mock.patch('chatgpt.views.Chatbot')
    def test_get_chat_list_view(self, mock_chatbot):
        chats = [
            {
                "id": "6aa9affa-940a-4994-be9d-da591573ade5",
                "title": "New chat",
                "create_time": "2023-05-25T02:47:29.715852+00:00",
                "update_time": "2023-05-25T02:47:31+00:00",
                "mapping": None,
                "current_node": None
            },
        ]

        mock_chatbot_instance = mock.Mock(spec=Chatbot)
        mock_chatbot.return_value = mock_chatbot_instance
        mock_chatbot_instance.get_conversations.return_value = chats

        client = Client()

        auth_headers = {"HTTP_AUTHORIZATION": 'token123'}

        response = client.get(
            '/conversations',
            **auth_headers
        )

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)

        self.assertEqual(data, chats)

        mock_chatbot.assert_called_once_with(
            config={"access_token": "token123"})
        mock_chatbot_instance.get_conversations.assert_called_once_with(
            limit=10,
            offset=0
        )
