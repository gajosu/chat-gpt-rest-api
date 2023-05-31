import json
from unittest import mock

from django.test import Client, RequestFactory, TestCase
from revChatGPT.V1 import Chatbot


class TestAskView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @mock.patch('chatgpt.views.Chatbot')
    def test_missing_prompt(self, mock_chatbot):

        client = Client()

        auth_headers = {"HTTP_AUTHORIZATION": 'token123'}

        response = client.post(
            '/conversations/123/ask',
            **auth_headers
        )

        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertEqual(data['error'], "prompt is required")

        mock_chatbot.assert_not_called()

    @mock.patch('chatgpt.views.Chatbot')
    def test_ask_view(self, mock_chatbot):
        mock_chatbot_instance = mock.Mock(spec=Chatbot)
        mock_chatbot.return_value = mock_chatbot_instance
        mock_chatbot_instance.ask.return_value = [
            {"message": "Hello World"},
        ]

        client = Client()
        auth_headers = {"HTTP_AUTHORIZATION": 'token123'}

        response = client.post(
            '/conversations/123/ask',
            {"prompt": "Hello"},
            **auth_headers
        )

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)

        self.assertEqual(data['response'], {"message": "Hello World"})

        mock_chatbot.assert_called_once_with(
            config={"access_token": "token123"})

        mock_chatbot_instance.ask.assert_called_once_with(
            prompt="Hello",
            conversation_id="123",
            parent_id="",
            model="",
            autocontinue=False
        )

    @mock.patch('chatgpt.views.Chatbot')
    def test_ask_with_optional_params(self, mock_chatbot):
        mock_chatbot_instance = mock.Mock(spec=Chatbot)
        mock_chatbot.return_value = mock_chatbot_instance
        mock_chatbot_instance.ask.return_value = [
            {"message": "Hello World"},
        ]

        client = Client()
        auth_headers = {"HTTP_AUTHORIZATION": 'token123'}

        response = client.post(
            '/conversations/123/ask',
            {
                "prompt": "Hello",
                "parent_id": "456",
                "model": "gpt-3.5-turbo",
                "autocontinue": "True"
            },
            **auth_headers
        )

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)

        self.assertEqual(data['response'], {"message": "Hello World"})

        mock_chatbot.assert_called_once_with(
            config={"access_token": "token123"})

        mock_chatbot_instance.ask.assert_called_once_with(
            prompt="Hello",
            conversation_id="123",
            parent_id="456",
            model="gpt-3.5-turbo",
            autocontinue=True
        )
