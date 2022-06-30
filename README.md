Необходимо разработать небольшой backend, который предоставляет REST API регистрации пользователя.

**Требования:**

1. Backend состоит из 3 микросервисов:
    - users
        - Реализует базовые операции над пользователями платформы:
            - **POST /v1/register/**
    - profile
        - Управляет профилями пользователей. Как правило в профиль включаются специфичные для бизнес-задач данные о пользователе. Например, ачивки, наличие подписки и пр.
    - emails
        - Отвечает за отправку писем.
2. Микросервисы оформлены в монорепу.
3. Деплой осуществляется с помощью Docker Compose.
4. (*) **Необязательно**, но будет плюсом:
    - Регистрация пользователя реализована в виде Saga ([https://microservices.io/patterns/data/saga.html](https://microservices.io/patterns/data/saga.html))

**Стек технологий:**

- Python 3
    - FastAPI
- PostgreSQL
- Docker
    - Docker Compose
- NGINX в качестве API Gateway


Test:
docker-compose up --build
curl  http://127.0.0.1:8007/v1/register/ -d '{"email":"j@vv.cc","first_name":"John","last_name":"Doe","active":"False","password":"x" }' -H "Content-Type: application/json" -X POST
curl  http://127.0.0.1:8007/v1/register/ -d '{"email":"qqj@vv.cc","first_name":"Jane","last_name":"Smith","active":"True","password":"x" }' -H "Content-Type: application/json" -X POST
curl  http://127.0.0.1:8007/v1/users/1
curl  http://127.0.0.1:8007/v1/users/2
curl  http://127.0.0.1:8007/v1/users/3
curl  http://127.0.0.1:8008/v1/profile/add/ -d '{"user_id": 1, "account_type":0, "iban":"XX1111111111111111111111"}' -H "Content-Type: application/json" -X POST
curl  http://127.0.0.1:8008/v1/profile/add/ -d '{"user_id": 2, "account_type":7, "iban":"YY2222222222222222222222"}' -H "Content-Type: application/json" -X POST
curl  http://127.0.0.1:8008/v1/profile/add/ -d '{"user_id": 3, "account_type":8, "iban":"YX2222222222222222222222"}' -H "Content-Type: application/json" -X POST
curl  http://127.0.0.1:8008/v1/profile/1
curl  http://127.0.0.1:8008/v1/profile/2
curl  http://127.0.0.1:8008/v1/subscription/add/ -d '{"user_id":1}' -H "Content-Type: application/json" -X POST
curl  http://127.0.0.1:8008/v1/subscription/add/ -d '{"user_id":2}' -H "Content-Type: application/json" -X POST
curl  http://127.0.0.1:8008/v1/subscription/1
curl  http://127.0.0.1:8008/v1/subscription/2
curl  http://127.0.0.1:8009/v1/emails/send/ -d '{"user_id":2, "subject":"SSSSSSS", "body":"Hi there!"}' -H "Content-Type: application/json" -X POST



Prod:
docker-compose -f docker-compose-prod.yml up --build
curl  http://127.0.0.1/v1/register/ -d '{"email":"j@vv.cc","first_name":"John","last_name":"Doe","active":"False","password":"x" }' -H "Content-Type: application/json" -X POST
curl  http://127.0.0.1/v1/register/ -d '{"email":"qqj@vv.cc","first_name":"Jane","last_name":"Smith","active":"True","password":"x" }' -H "Content-Type: application/json" -X POST
curl  http://127.0.0.1/v1/users/1
curl  http://127.0.0.1/v1/users/2
curl  http://127.0.0.1/v1/users/3
curl  http://127.0.0.1/v1/profile/add/ -d '{"user_id": 1, "account_type":0, "iban":"XX1111111111111111111111"}' -H "Content-Type: application/json" -X POST
curl  http://127.0.0.1/v1/profile/add/ -d '{"user_id": 2, "account_type":7, "iban":"YY2222222222222222222222"}' -H "Content-Type: application/json" -X POST
curl  http://127.0.0.1/v1/profile/add/ -d '{"user_id": 3, "account_type":8, "iban":"YX2222222222222222222222"}' -H "Content-Type: application/json" -X POST
curl  http://127.0.0.1/v1/profile/1
curl  http://127.0.0.1/v1/profile/2
curl  http://127.0.0.1/v1/subscription/add/ -d '{"user_id":1}' -H "Content-Type: application/json" -X POST
curl  http://127.0.0.1/v1/subscription/add/ -d '{"user_id":2}' -H "Content-Type: application/json" -X POST
curl  http://127.0.0.1/v1/subscription/1
curl  http://127.0.0.1/v1/subscription/2
curl  http://127.0.0.1/v1/emails/send/ -d '{"user_id":2, "subject":"SSSSSSS", "body":"Hi there!"}' -H "Content-Type: application/json" -X POST
