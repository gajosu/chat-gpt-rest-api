import json
from unittest import mock

from django.test import Client, TestCase, override_settings
from revChatGPT.typings import Error as ChatbotError
from revChatGPT.V1 import Chatbot


class TestErrorHandlerMiddleware(TestCase):

    @mock.patch('chatgpt.views.Chatbot')
    def test_open_ai_error_handler(self, mock_chatbot):
        """
        Test that the error handler middleware catches OpenAIAuth errors and returns a 500 response
        """
        with override_settings(
            MIDDLEWARE=['chatgpt.middleware.error_handler.ErrorHandlerMiddleware']
            ):
            client = Client()

            mock_chatbot_instance = mock.Mock(spec=Chatbot)
            mock_chatbot.return_value = mock_chatbot_instance

            error_response = {
                "location": "location",
                "status_code": 500,
                "details": "details"
            }

            mock_chatbot_instance.ask.side_effect = ChatbotError(
                source="source",
                message=json.dumps(error_response),
            )

            response = client.post(
                path='/conversations/new',
                data={'prompt': 'Hello'},
            )

            self.assertEqual(response.status_code, 500)

            data = json.loads(response.content)

            self.assertEqual(data['error'], error_response)
