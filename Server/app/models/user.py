from mongoengine import *
from werkzeug.security import check_password_hash, generate_password_hash

from app.models import Base


class UserModel(Base):
    meta = {
        'collection': 'user'
    }

    id = StringField(
        primary_key=True,
        min_length=4,
        max_length=50
    )

    pw = StringField(
        required=True
    )

    email = StringField(
        required=True
    )

    name = StringField(
        required=True,
        min_length=2,
        max_length=16
    )

    nickname = StringField(
        required=False,
        min_length=1,
        max_length=30
    )

    bio = StringField(
        required=False,
        min_length=1,
        max_length=85
    )

    @classmethod
    def is_id_exist(cls, id):
        return bool(cls.objects(id=id))

    @classmethod
    def is_email_exist(cls, email):
        return bool(cls.objects(email=email))

    @classmethod
    def signup(cls, id, plain_pw, email, name, nickname=None, bio=None):
        if cls.is_id_exist(id):
            return

        if cls.is_email_exist(email):
            return

        return cls(
            id=id,
            pw=generate_password_hash(plain_pw),
            email=email,
            name=name,
            nickname=nickname,
            bio=bio
        ).save()

    @classmethod
    def get_user_as_login(cls, id: str, plain_pw: str):
        user = cls.objects(id=id).first()

        if not user:
            return
        else:
            if check_password_hash(user.pw, plain_pw):
                return user
            else:
                return
