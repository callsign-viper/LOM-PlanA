from uuid import UUID, uuid4
from typing import Callable

from flask import abort
from flask_jwt_extended import create_access_token, create_refresh_token
from mongoengine import *

from app.models import Base
from app.models.user import UserModel


class TokenBase(Base):
    meta = {
        'abstract': True,
        'allow_inheritance': True
    }

    class Key(EmbeddedDocument):
        owner = ReferenceField(
            document_type=UserModel,
            required=True
        )

        user_agent = StringField(
            required=True
        )

    key = EmbeddedDocumentField(
        document_type=Key,
        primary_key=True
    )
    # 여러 필드를 합쳐 PK로 두기 위함

    client_ip = StringField(
        required=True
    )

    identity = UUIDField(
        unique=True,
        default=uuid4
    )

    @classmethod
    def _create_token(cls, create_token_func: Callable, user: UserModel, user_agent: str, remote_addr: str):
        """
        Create token with `create_token_func`

        Args:
            create_token_func: token creation function in `flask_jwt_extended.utils`
            user: instance from UserModel
            user_agent: user agent of requested user ex) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100
            remote_addr: remote ip address of requested user(x.x.x.x)
        """

        key = cls.Key(owner=user, user_agent=user_agent)
        cls.objects(key=key).delete()

        token = cls(
            key=key,
            client_ip=remote_addr
        ).save()

        identity = token.identity

        return create_token_func(str(identity))

    @classmethod
    def _get_token_with_validation(cls, identity: str, user_agent: str, remote_addr: str):
        """
        Get token with validate token.
            aborts
            - 401 when `identity` is invalid
            - 403 when the 'information of the requester' and the 'information of the token' are inconsistent
            - 422 when `identity` can not be parsed as a UUID

        Args:
            identity: 'identity' claim's data of JWT payload
            user_agent: user agent of requested user
            remote_addr: remote ip address of requested user
        """

        try:
            token = cls.objects(identity=UUID(identity)).first()

            if not token:
                abort(401, 'invalid identity.')

            if token.key.user_agent != user_agent or token.client_ip != remote_addr:
                # token generation 당시의 정보와 대조
                abort(403)

            return token

        except ValueError:
            abort(422, 'token identity is invalid.')


class AccessTokenModel(TokenBase):
    meta = {
        'collection': 'access_token'
    }

    @classmethod
    def create_token(cls, user, user_agent, remote_addr):
        return cls._create_token(create_access_token, user, user_agent, remote_addr)

    @classmethod
    def get_token_with_validation(cls, identity, user_agent, remote_addr):
        return cls._get_token_with_validation(identity, user_agent, remote_addr)


class RefreshTokenModel(TokenBase):
    meta = {
        'collection': 'refresh_token'
    }

    @classmethod
    def create_token(cls, user, user_agent, remote_addr):
        return cls._create_token(create_refresh_token, user, user_agent, remote_addr)

    @classmethod
    def refresh(cls, identity, user_agent, remote_addr):
        token = cls._get_token_with_validation(identity, user_agent, remote_addr)

        return cls.create_token(token.key.owner, user_agent, remote_addr)
