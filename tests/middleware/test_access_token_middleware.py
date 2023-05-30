import json
from unittest import mock

from django.test import Client, RequestFactory, TestCase, override_settings


class TestAccessTokenMiddlewares(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @mock.patch('chatgpt.views.Chatbot')
    def test_ask_view_missing_access_token(self, mock_chatbot):
        """
        Test that the access token middleware returns a 401 response if the access token is missing
        """
        with override_settings(
            MIDDLEWARE=['chatgpt.middleware.access_token.AccessTokenMiddleware']
            ):
            client = Client()

            response = client.post('/conversations')

            self.assertEqual(response.status_code, 401)
            data = json.loads(response.content)
            self.assertEqual(data['error'], "access_token is required")

            mock_chatbot.assert_not_called()
