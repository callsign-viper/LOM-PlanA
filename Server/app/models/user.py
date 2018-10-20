from typing import Union

from mongoengine import *
from werkzeug.exceptions import Conflict
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

    # is_id_exist = classmethod(lambda cls, id: bool(cls.objects(id=id)))
    @classmethod
    def is_id_exist(cls, id: str) -> bool:
        """
        Check `id` is already exist in collection.

        Args:
            id: ID for check

        Returns:
            True if ID already exists, otherwise False.
        """

        return bool(cls.objects(id=id))

    # is_email_exist = classmethod(lambda cls, email: bool(cls.objects(email=email)))
    @classmethod
    def is_email_exist(cls, email: str) -> bool:
        """
        Check `email` is already exist in collection.

        Args:
            email: email for check

        Returns:
            True if email already exists, otherwise False.
        """

        return bool(cls.objects(email=email))

    @classmethod
    def signup(cls, id: str, plain_pw: str, email: str, name: str, nickname: str=None, bio: str=None) -> 'UserModel':
        """
        Creates new user.

        Args:
            id: ID of user
            plain_pw : Password of user as plain text
            email: Email of user
            name: Name of user
            nickname: Nickname of user
            bio: Bio of user

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
    def get_user_as_login(cls, id: str, plain_pw: str) -> Union['UserModel', None]:
        """
        Get user as login with `id`, `plain_pw`

        Args:
            id: ID of user
            plain_pw : Password of user as plain text
        """

        user = cls.objects(id=id).first()

        if not user:
            return
        else:
            if check_password_hash(user.pw, plain_pw):
                return user
            else:
                return
