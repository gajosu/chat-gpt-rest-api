from unittest import mock

from django.http import HttpResponse
from django.test import RequestFactory, TestCase
from revChatGPT.V1 import Chatbot

from chatgpt.views import delete_conversation


class TestViews(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

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
