import json
from django.test import TestCase, RequestFactory
from django.http import JsonResponse, HttpResponse
from unittest import mock
from revChatGPT.V1 import Chatbot
from chatgpt.views import ask, delete_conversation

class MyViewsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @mock.patch('chatgpt.views.Chatbot')
    def test_ask_view_missing_access_token(self, mock_chatbot):
        request = self.factory.post(path='/ask', data={
            'prompt': 'Hello'
        },
        QUERY_STRING='conversation_id=123')

        response = ask(request)

        self.assertEqual(response.status_code, 401)
        data = json.loads(response.content)
        self.assertEqual(data['error'], "access_token is required")

        mock_chatbot.assert_not_called()

    @mock.patch('chatgpt.views.Chatbot')
    def test_ask_view_missing_prompt(self, mock_chatbot):
        request = self.factory.post(path='/ask', data={
            'conversation_id': '123'
        })
        request.META['HTTP_AUTHORIZATION'] = 'token123'

        response = ask(request)

        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertEqual(data['error'], "prompt is required")

        mock_chatbot.assert_not_called()

    @mock.patch('chatgpt.views.Chatbot')
    def test_ask_view(self, mock_chatbot):
        mock_chatbot_instance = mock.Mock(spec=Chatbot)
        mock_chatbot.return_value = mock_chatbot_instance
        mock_chatbot_instance.ask.return_value = [
            {"message": "Hello"},
            {"message": "World"}
        ]

        request = self.factory.post(path='/ask', data={
            'prompt': 'Hello'
        },
        QUERY_STRING='conversation_id=123')
        request.META['HTTP_AUTHORIZATION'] = 'token123'

        response = ask(request)

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)

        self.assertEqual(data['response'], {"message": "World"})

        mock_chatbot.assert_called_once_with(config={"access_token": "token123"})
        mock_chatbot_instance.ask.assert_called_once_with("Hello", "123")

    @mock.patch('chatgpt.views.Chatbot')
    def test_delete_conversation_view(self, mock_chatbot):
        mock_chatbot_instance = mock.Mock(spec=Chatbot)
        mock_chatbot.return_value = mock_chatbot_instance

        request = self.factory.delete('/delete_conversation/123')
        request.META['HTTP_AUTHORIZATION'] = 'token123'

        response = delete_conversation(request, conversation_id='123')

        self.assertEqual(response.status_code, 204)
        self.assertIsInstance(response, HttpResponse)

        mock_chatbot.assert_called_once_with(config={"access_token": "token123"})
        mock_chatbot_instance.delete_conversation.assert_called_once_with('123')
