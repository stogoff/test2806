import asyncpg
from fastapi import FastAPI, Response, status

from db import database, Profile, Subscription

app = FastAPI(title="Profile Service")


@app.on_event("startup")
async def startup():
    if not database.is_connected:
        await database.connect()
    # create a dummy entry
    # await User.objects.get_or_create(email="test1@test.com")


@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()


@app.post("/v1/profile/add/")
async def add_profile(profile: Profile, response: Response):
    try:
        created = await Profile.objects.get_or_create(user_id=profile.user_id,
                                                      account_type=profile.account_type,
                                                      iban=profile.iban
                                                      )
        return created
    except asyncpg.exceptions.ForeignKeyViolationError:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "user not found"}


@app.post("/v1/subscription/add/")
async def add_subscription(sub: Subscription, response: Response):
    try:
        created_sub = await Subscription.objects.get_or_create(user_id=sub.user_id)
        return created_sub
    except asyncpg.exceptions.ForeignKeyViolationError:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "user not found"}


@app.get("/v1/profile/{user_id}")
async def show_profile(user_id: int):
    return await Profile.objects.all(user_id=user_id)


@app.get("/v1/subscription/{user_id}")
async def show_profile(user_id: int):
    return await Subscription.objects.all(user_id=user_id)
