from fastapi import FastAPI, Response, status

from db import database, User
from ormar import exceptions

app = FastAPI(title="User Service")


@app.on_event("startup")
async def startup():
    if not database.is_connected:
        await database.connect()


@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()


@app.get("/v1/users/{user_id}")
async def show_profile(user_id: int, response: Response):
    try:
        user = await User.objects.get(id=user_id)
        return user
    except exceptions.NoMatch:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "user not found"}


@app.post("/v1/register/")
async def create_user(user: User):
    return await User.objects.get_or_create(email=user.email,
                                            first_name=user.first_name,
                                            last_name=user.last_name,
                                            active=user.active,
                                            password=user.password)
