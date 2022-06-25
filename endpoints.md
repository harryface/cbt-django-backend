
## Register

```http
POST /account/register/
```

### Request Body

```javascript
{
  "first_name": "string",
  "last_name": "string",
  "email": "user@example.com",
  "password": "string",
  "password_confirm": "string"
}
```

### Response

```javascript
{
  "id": 0,
  "first_name": "string",
  "last_name": "string",
  "email": "user@example.com"
}
```

## Reset Account

```http
POST /account/reset/
```

### Request Body

```javascript
{
  "email": "user@example.com"
}
```

### Response

```javascript
{
  "message": "if your account exists, we have sent you a mail"
}
```


## Change Account Password

```http
POST /account/reset/change_password/
```

### Request Body

```javascript
{
  "secret": "string",
  "password": "string"
}
```

### Response

```javascript
{
  "success": "Passwod changed successfully."
}
```


## Login

```http
POST /api/token/
```

### Authorization: No Auth

### Request Body

```javascript
{
  "email" : string,
  "password" : string
}
```

### Response

```javascript
{
  "refresh": "string",
  "access": "string"
}
```

## Refresh Token

```http
POST /api/token/refresh/
```

### Authorization: No Auth

### Request Body

```javascript
{
  "refresh" : string
}
```

### Response
```javascript
{
  "access": "string"
}
```

## Submit Exam Answers

```http
POST /core/answer/
```

### Request Body

```javascript
[
  {
    "question": 0,
    "answer": "string"
  }
]
```

### Response

```javascript
[
  {
    "id": 0,
    "taker": 0,
    "question": 0,
    "answer": "string"
  }
]
```

## List Exams

```http
GET /core/exam/
```

### Response

```javascript
[
  {
    "id": 0,
    "title": "string",
    "duration": 0,
    "instructions": "string",
    "questions": [
      {
        "id": 0,
        "image": "string",
        "question": "string",
        "option_1": "string",
        "option_2": "string",
        "option_3": "string",
        "option_4": "string",
        "option_5": "string"
      }
    ],
    "created_at": "2022-06-25T22:47:33.508Z"
  }
]
```

## Retrieve Exams

```http
GET /core/exam/{id}
```

### Response

```javascript
{
  "id": 0,
  "title": "string",
  "duration": 0,
  "instructions": "string",
  "questions": [
    {
      "id": 0,
      "image": "string",
      "question": "string",
      "option_1": "string",
      "option_2": "string",
      "option_3": "string",
      "option_4": "string",
      "option_5": "string"
    }
  ],
  "created_at": "2022-06-25T22:48:40.713Z"
}
```

## Create Exams

```http
POST /core/exam/
```

### Request Body

```javascript
{
  "title": "string",
  "duration": 0,
  "instructions": "string",
  "questions": [
    {
      "image": "string",
      "question": "string",
      "option_1": "string",
      "option_2": "string",
      "option_3": "string",
      "option_4": "string",
      "option_5": "string",
      "answer": "string"
    }
  ],
  "students": [
    0
  ]
}
```

### Response

```javascript
{
  "id": 0,
  "title": "string",
  "duration": 0,
  "instructions": "string",
  "questions": [
    {
      "id": 0,
      "image": "string",
      "question": "string",
      "option_1": "string",
      "option_2": "string",
      "option_3": "string",
      "option_4": "string",
      "option_5": "string"
    }
  ],
  "created_at": "2022-06-25T22:49:48.275Z"
}
```

## Patch Exams

```http
PATCH /core/exam/
```

### Request Body

```javascript
{
  "title": "string",
  "duration": 0,
  "instructions": "string",
  "questions": [
    {
      "image": "string",
      "question": "string",
      "option_1": "string",
      "option_2": "string",
      "option_3": "string",
      "option_4": "string",
      "option_5": "string",
      "answer": "string"
    }
  ],
  "students": [
    0
  ]
}
```

### Response

```javascript
{
  "id": 0,
  "title": "string",
  "duration": 0,
  "instructions": "string",
  "questions": [
    {
      "id": 0,
      "image": "string",
      "question": "string",
      "option_1": "string",
      "option_2": "string",
      "option_3": "string",
      "option_4": "string",
      "option_5": "string"
    }
  ],
  "created_at": "2022-06-25T22:52:38.436Z"
}
```

## Delete Exams

```http
DELETE /core/exam/{id}
```

## Retrieve Exam Result

```http
GET /core/exam/{id}/result/
```

### Response

```javascript
{
  "total_questions": "string",
  "attempted_questions": "string",
  "correct_answers": "string",
  "wrong_answers": "string",
  "percentage": "string"
}
```

###ACCOUNT routes###

account/register/
account/reset/
account/reset/change_password/


###API routes###

api/token/
api/token/refresh/


###CORE routes###

core/answer/
core/exam/<int: exam_pk>/
core/exam/<int: exam_pk>/
core/exam/<int: exam_pk>/
core/exam/<int: exam_pk>/
core/exam/<int: exam_pk>/
core/exam/<int: exam_pk>/result
core/exam/