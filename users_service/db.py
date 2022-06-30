from typing import Optional, Union, Dict

import databases
import ormar
import sqlalchemy.exc
import datetime

from config import settings

database = databases.Database(settings.db_url)
metadata = sqlalchemy.MetaData()


def now_plus_year():
    return datetime.datetime.now() + datetime.timedelta(weeks=52)

class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


class User(ormar.Model):
    class Meta(BaseMeta):
        tablename = "users"

    id: int = ormar.Integer(primary_key=True)
    first_name: str = ormar.String(max_length=128, unique=False, nullable=False)
    last_name: str = ormar.String(max_length=128, unique=False, nullable=False)
    email: str = ormar.String(max_length=128, unique=True, nullable=False)
    password: str = ormar.String(max_length=128, unique=False, nullable=False)
    active: bool = ormar.Boolean(default=True, nullable=False)


class Profile(ormar.Model):
    class Meta(BaseMeta):
        tablename = "profiles"

    id: int = ormar.Integer(primary_key=True)
    user_id: Optional[Union[User, Dict]] = ormar.ForeignKey(User)
    account_type: int = ormar.Integer()
    iban: str = ormar.String(max_length=34)


class Subscription(ormar.Model):
    class Meta(BaseMeta):
        tablename = "subscriptions"

    id: int = ormar.Integer(primary_key=True)
    user_id: Optional[Union[User, Dict]] = ormar.ForeignKey(User)
    starts_at: datetime.datetime = ormar.DateTime(
        default=datetime.datetime.now
    )
    expires_at: datetime.datetime = ormar.DateTime(
        default=now_plus_year
    )


engine = sqlalchemy.create_engine(settings.db_url,
                                  pool_pre_ping=True,
                                  pool_recycle=3600,
                                  connect_args={
                                      "keepalives": 1,
                                      "keepalives_idle": 30,
                                      "keepalives_interval": 10,
                                      "keepalives_count": 5, })
try:
    metadata.create_all(engine, checkfirst=True)
except:
    pass
