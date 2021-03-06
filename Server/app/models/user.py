from mongoengine import *
from werkzeug.exceptions import Conflict, NotFound, Unauthorized
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

    email = EmailField(
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
    def is_id_exist(cls, id: str) -> bool:
        """
        Returns:
            True if ID already exists, otherwise False.
        """

        return bool(cls.objects(id=id))

    @classmethod
    def is_email_exist(cls, email: str) -> bool:
        """
        Returns:
            True if email already exists, otherwise False.
        """

        return bool(cls.objects(email=email))

    @classmethod
    def signup(cls, id: str, plain_pw: str, email: str, name: str, nickname: str=None, bio: str=None) -> 'UserModel':
        """
        Raises:
            Conflict: ID or email is already existing.
        """

        if cls.is_id_exist(id):
            raise Conflict('ID {} already exists.'.format(id))

        if cls.is_email_exist(email):
            raise Conflict('Email {} already exists.'.format(email))

        return cls(
            id=id,
            pw=generate_password_hash(plain_pw),
            email=email,
            name=name,
            nickname=nickname,
            bio=bio
        ).save()

    @classmethod
    def get_user_as_login(cls, id: str, plain_pw: str) -> 'UserModel':
        """
        Raises:
            Unauthorized: Can't find user
        """

        user = cls.objects(id=id).first()

        if not user:
            raise Unauthorized('Invalid ID')
        else:
            if check_password_hash(user.pw, plain_pw):
                return user
            else:
                raise Unauthorized('Invalid PW')

    @classmethod
    def get_user_with_id(cls, id: str) -> 'UserModel':
        """
        Raises:
            NotFound: Can't find user
        """

        user = cls.objects(id=id).first()

        if not user:
            raise NotFound('There\'s no any user with ID : {}'.format(id))

        return user
