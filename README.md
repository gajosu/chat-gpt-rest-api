# Chat GPT REST API

This project provides a REST API for interacting with Chat GPT, a conversational AI powered by GPT. It allows you to send prompts and receive responses from the Chat GPT model.

## Endpoints

### Ask Endpoint

#### URL

POST `/ask`


#### Request Parameters

| Parameter        | Type   | Required | Description                            |
|------------------|--------|----------|----------------------------------------|
| `prompt`         | string | Yes      | The prompt message for the conversation |
| `conversation_id`| string | No       | The ID of the conversation (optional)   |

#### Request Headers

| Header          | Description                           |
|-----------------|---------------------------------------|
| `Authorization` | Access token for authentication       |

#### Response

- Status Code: 200 OK
- Content-Type: application/json

Example Response Body:
```json
{
    "response": {
        "message": "Hello, how can I assist you?"
    }
}
```

### Delete Conversation Endpoint

#### URL

DELETE `/conversation/{conversation_id}`

#### Path Parameters

| Parameter        | Type   | Required | Description                            |
|------------------|--------|----------|----------------------------------------|
| `conversation_id`| string | Yes      | The ID of the conversation             |

#### Request Headers

| Header          | Description                           |
|-----------------|---------------------------------------|
| `Authorization` | Access token for authentication       |

#### Response

- Status Code: 204 No Content


## Authentication
The API requires authentication using an access token. You need to include the Authorization header with the value set to your access token in each request.


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

3. You can now send requests to the API at `http://localhost:8000/ask`


## License

This project is licensed under the terms of the MIT license. See the [LICENSE](LICENSE) file for details.