import json
from unittest import mock

from django.test import Client, RequestFactory, TestCase
from revChatGPT.V1 import Chatbot


class TestMessagesView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @mock.patch('chatgpt.views.Chatbot')
    def test_get_messages_of_a_conversation_view(self, mock_chatbot):
        conversation_id = '123'

        messages = [
            {
                "title": "New chat",
                "create_time": 1684982849.715852,
                "update_time": 1684982851,
                "mapping": {
                    "6d35a3e1-9414-4316-a850-1f56ff0a3c5c": {
                        "id": "6d35a3e1-9414-4316-a850-1f56ff0a3c5c",
                        "message": {
                            "id": "6d35a3e1-9414-4316-a850-1f56ff0a3c5c",
                            "author": {
                                "role": "system",
                                "metadata": {}
                            },
                            "create_time": 1684982849.716171,
                            "content": {
                                "content_type": "text",
                                "parts": [
                                    ""
                                ]
                            },
                            "status": "finished_successfully",
                            "weight": 1,
                            "metadata": {},
                            "recipient": "all"
                        },
                        "parent": "37fb775c-6369-4326-a248-b092ed9a5239",
                        "children": [
                            "35619ca2-43be-46cf-bfc7-4b7306a427bd"
                        ]
                    },
                }
            }]

        mock_chatbot_instance = mock.Mock(spec=Chatbot)
        mock_chatbot.return_value = mock_chatbot_instance
        mock_chatbot_instance.get_msg_history.return_value = messages

        client = Client()

        auth_headers = {"HTTP_AUTHORIZATION": 'token123'}

        response = client.get(
            '/conversations/' + conversation_id + '/messages',
            **auth_headers
        )

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)

        self.assertEqual(data, messages)

        mock_chatbot.assert_called_once_with(
            config={"access_token": "token123"})
        mock_chatbot_instance.get_msg_history.assert_called_once_with(
            convo_id=conversation_id)
