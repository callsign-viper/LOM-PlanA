from werkzeug.security import check_password_hash, generate_password_hash

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

    @classmethod
    def is_id_exist(cls, id):
        return bool(cls.objects(id=id))

    @classmethod
    def signup(cls, id, plain_pw, name, nickname=None, bio=None):
        if cls.is_id_exist(id):
            return False

        return cls(
            id=id,
            pw=generate_password_hash(plain_pw),
            name=name,
            nickname=nickname,
            bio=bio
        ).save()

    @classmethod
    def certify(cls, id, plain_pw):
        user = cls.objects(id=id).first()

        if not user:
            return False
        else:
            if check_password_hash(user.pw, plain_pw):
                return user
            else:
                return False
