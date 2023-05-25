from unittest import mock

from django.http import HttpResponse
from django.test import Client, RequestFactory, TestCase
from revChatGPT.V1 import Chatbot


class TestDeleteConversationView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @mock.patch('chatgpt.views.Chatbot')
    def test_delete_conversation_view(self, mock_chatbot):
        mock_chatbot_instance = mock.Mock(spec=Chatbot)
        mock_chatbot.return_value = mock_chatbot_instance

        client = Client()
        auth_headers = {"HTTP_AUTHORIZATION": 'token123'}
        response = client.delete(
            '/conversations/123',
            **auth_headers
        )

        self.assertEqual(response.status_code, 204)
        self.assertIsInstance(response, HttpResponse)

        mock_chatbot.assert_called_once_with(
            config={"access_token": "token123"})
        mock_chatbot_instance.delete_conversation.assert_called_once_with(
            '123')
