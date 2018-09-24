from app.extensions import mongoengine
from app.models import Base


class UserModel(Base):
    meta = {
        'collection': 'user'
    }

    id = mongoengine.StringField(
        primary_key=True,
        min_length=4,
        max_length=50
    )

    pw = mongoengine.StringField(
        required=True
    )

    name = mongoengine.StringField(
        required=True,
        min_length=2,
        max_length=16
    )

    nickname = mongoengine.StringField(
        required=False,
        min_length=1,
        max_length=30
    )

    bio = mongoengine.StringField(
        required=False,
        min_length=1,
        max_length=85
    )

