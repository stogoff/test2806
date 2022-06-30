import datetime

from fastapi import FastAPI, Response, status
from pydantic import BaseModel

from db import database, User, Subscription

app = FastAPI(title="Email Service")


class Message(BaseModel):
    user_id: int
    subject: str
    body: str


async def send_msg(email, subj, body):
    return {"result": f"message sent to {email} with subject {subj} and length {len(body)}"}


@app.post("/v1/emails/send/")
async def send_mail(msg: Message, response: Response):
    user = await User.objects.get(id=msg.user_id)
    if user:
        email = user.email
        active = user.active
        subs = await Subscription.objects.all(user_id=msg.user_id)
        for s in subs:
            if s.starts_at < datetime.datetime.now() < s.expires_at and active:
                return await send_msg(email, msg.subject, msg.body)
        response.status_code = status.HTTP_406_NOT_ACCEPTABLE
        return {"error": "nothing to send"}
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "user not found"}


@app.on_event("startup")
async def startup():
    if not database.is_connected:
        await database.connect()
    # create a dummy entry
    # await User.objects.get_or_create(email="test@test.com")


@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()
