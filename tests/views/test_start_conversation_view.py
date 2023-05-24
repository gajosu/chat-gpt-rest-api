import json
from unittest import mock

from django.test import RequestFactory, TestCase
from revChatGPT.V1 import Chatbot

from chatgpt.views import start_new_conversation


class TestViews(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @mock.patch('chatgpt.views.Chatbot')
    def test_missing_prompt(self, mock_chatbot):
        request = self.factory.post(path='/conversations', data={
            'conversation_id': '123'
        })
        request.META['HTTP_AUTHORIZATION'] = 'token123'

        response = start_new_conversation(request)

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

        request = self.factory.post(path='/conversations', data={
            'prompt': 'Hello'
        })
        request.META['HTTP_AUTHORIZATION'] = 'token123'

        response = start_new_conversation(request)

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)

        self.assertEqual(data['response'], {"message": "Hello World"})

        mock_chatbot.assert_called_once_with(config={"access_token": "token123"})
        mock_chatbot_instance.ask.assert_called_once_with("Hello")