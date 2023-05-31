import json
from unittest import mock

from django.test import Client, RequestFactory, TestCase
from revChatGPT.V1 import Chatbot


class TestStartConversationView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @mock.patch('chatgpt.views.Chatbot')
    def test_missing_prompt(self, mock_chatbot):

        client = Client()

        auth_headers = {"HTTP_AUTHORIZATION": 'token123'}

        response = client.post(
            '/conversations/new',
            **auth_headers
        )

        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertEqual(data['error'], "prompt is required")

        mock_chatbot.assert_not_called()

    @mock.patch('chatgpt.views.Chatbot')
    def test_new_conversation_view(self, mock_chatbot):
        mock_chatbot_instance = mock.Mock(spec=Chatbot)
        mock_chatbot.return_value = mock_chatbot_instance
        mock_chatbot_instance.ask.return_value = [
            {"message": "Hello World"},
        ]
        mock_chatbot_instance.change_title.return_value = None

        client = Client()
        auth_headers = {"HTTP_AUTHORIZATION": 'token123'}

        response = client.post(
            '/conversations/new',
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
            model="",
            autocontinue=False
        )
        mock_chatbot_instance.change_title.assert_not_called()

    @mock.patch('chatgpt.views.Chatbot')
    def test_new_conversation_with_title(self, mock_chatbot):
        mock_chatbot_instance = mock.Mock(spec=Chatbot)
        mock_chatbot.return_value = mock_chatbot_instance
        mock_chatbot_instance.ask.return_value = [
            {
                "message": "Hello World",
                "conversation_id": "123"
            },
        ]
        mock_chatbot_instance.change_title.return_value = None

        client = Client()
        auth_headers = {"HTTP_AUTHORIZATION": 'token123'}

        response = client.post(
            '/conversations/new',
            {"prompt": "Hello", "title": "My Title"},
            **auth_headers
        )

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)

        self.assertEqual(data['response'], {
            "message": "Hello World",
            "conversation_id": "123"
        })

        mock_chatbot.assert_called_once_with(
            config={"access_token": "token123"})

        mock_chatbot_instance.ask.assert_called_once_with(
            prompt="Hello",
            model="",
            autocontinue=False
        )
        mock_chatbot_instance.change_title.assert_called_once_with("123", "My Title")

    @mock.patch('chatgpt.views.Chatbot')
    def test_new_conversation_with_model_and_autocontinue(self, mock_chatbot):
        mock_chatbot_instance = mock.Mock(spec=Chatbot)
        mock_chatbot.return_value = mock_chatbot_instance
        mock_chatbot_instance.ask.return_value = [
            {"message": "Hello World"},
        ]

        client = Client()
        auth_headers = {"HTTP_AUTHORIZATION": 'token123'}

        response = client.post(
            '/conversations/new',
            {
                "prompt": "Hello",
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
            model="gpt-3.5-turbo",
            autocontinue=True
        )
