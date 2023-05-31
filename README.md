# Chat GPT REST API

This project provides a REST API for interacting with Chat GPT, a conversational AI powered by GPT. It allows you to send prompts and receive responses from the Chat GPT model.


## Content Table
- [Api documentation](#api-documentation)
  - [Get Conversations](#get-conversations)
  - [New Conversation](#new-conversation)
  - [Ask](#ask)
  - [Delete Conversation](#delete-conversation)
  - [Delete All Conversations](#delete-all-conversations)
  - [Get Messages](#get-messages)



## Api documentation

### Get Conversations

Return a list of conversations.

GET `/conversations`

Response: `200`
```json
[
  {
    "id": "d6bd2590-01f4-32b7-b1y3-c5ea1fr7r819",
    "title": "Conversation 1",
    "create_time": "2023-05-28T17:13:08.233528+00:00",
    "update_time": "2023-05-28T17:13:24+00:00",
    "mapping": null,
    "current_node": null
  },
  ...
]
```
### New Conversation

Create a new conversation and ask the first question.

POST `/conversations/new`

## Request Body

| Parameter        | Type   | Required | Description                            |
|------------------|--------|----------|----------------------------------------|
| `prompt`         | string | Yes      | The prompt message for the conversation |
| `title`          | string | No       | The title of the conversation |
| `model`          | string | No       | The model to use for the conversation |
| `autocontinue`   | string | No       | Whether to automatically continue the conversation, must be `true` or `false` |

Response: `201`
```json
{
  "response": {
    "author": {
      "role": "assistant",
      "name": null,
      "metadata": {}
    },
    "message": "¡Sure, I can help you with that! What is your name?",
    "conversation_id": "c6b0aeef-b322-4f47-a9f8-7e52ebca942a",
    "parent_id": "07cd64d2-da49-4b39-a652-a69b31eede06",
    "model": "text-davinci-002-render-sha",
    "finish_details": "stop",
    "end_turn": false,
    "recipient": "all",
    "citations": []
  }
}
```

### Ask

Ask a question to the conversation.

POST `/conversations/{conversation_id}/ask`

#### Body Parameters

| Parameter        | Type   | Required | Description                            |
|------------------|--------|----------|----------------------------------------|
| `prompt`         | string | Yes      | The prompt message for the conversation |
| `parent_id`      | string | No       | UUID for the message to continue on |
| `model`          | string | No       | The model to use for the conversation |
| `autocontinue`   | string | No       | Whether to automatically continue the conversation, must be `true` or `false` |


Response: `201`
```json
{
  "response": {
    "author": {
      "role": "assistant",
      "name": null,
      "metadata": {}
    },
    "message": "¡Sure, I can help you with that! What is your name?",
    "conversation_id": "c6b0aeef-b322-4f47-a9f8-7e52ebca942a",
    "parent_id": "07cd64d2-da49-4b39-a652-a69b31eede06",
    "model": "text-davinci-002-render-sha",
    "finish_details": "stop",
    "end_turn": false,
    "recipient": "all",
    "citations": []
  }
}
```

### Delete Conversation

Delete a conversation.
#### URL

DELETE `/conversations/{conversation_id}`

Response: `204 No Content`


### Delete All Conversations

Delete all conversations.

DELETE `/conversations/all`

Response: `204 No Content`

### Get Messages

Get all messages from a conversation.

GET `/conversations/{conversation_id}/messages`

Response: `200`
```json
[
  {
    "author": {
      "role": "assistant",
      "name": null,
      "metadata": {}
    },
    "message": "¡Sure, I can help you with that! What is your name?",
    "conversation_id": "c6b0aeef-b322-4f47-a9f8-7e52ebca942a",
    "parent_id": "07cd64d2-da49-4b39-a652-a69b31eede06",
    "model": "text-davinci-002-render-sha",
    "finish_details": "stop",
    "end_turn": false,
    "recipient": "all",
    "citations": []
  },
  ...
]
```

## Authentication
The API requires authentication using an access token. You need to include the Authorization header with the value set to your access token in each request.
#### Request Headers

| Header          | Description                           |
|-----------------|---------------------------------------|
| `Authorization` | Access token for authentication       |

For obtaining an access token, you need be logged in to your OpenAI account and go to the sesion endpoint.

https://chat.openai.com/api/auth/session

Copy the value of the `accessToken` field and use it as the value of the Authorization header.

## Rate Limiting

OpenAI has a rate limit of 50 requests per hour. If you exceed this limit, you will receive a `500` response code with the error message `Rate limit exceeded`.

## Getting Started

To get started with the Chat GPT API, follow these steps:

1. Install the required dependencies by running:
    ```bash
    pip install -r requirements.txt
    ```

2. Run the server:
    ```bash
    python manage.py runserver
    ```

3. You can now send requests to the API at `http://localhost:8000`


## License

This project is licensed under the terms of the GPL-2.0 license. See the [LICENSE](LICENSE) file for details.

## Disclaimers

This project is in no way affiliated with, associated with, authorized by, endorsed by, or officially affiliated in any way with OpenAI, Inc. (www.openai.com).
This project uses a public npm package called [revChatGPT](https://github.com/acheong08/ChatGPT) to interact with the OpenAI API.
I am not responsible for possible bans or suspensions of your OpenAI account. Use this project at your own risk.
