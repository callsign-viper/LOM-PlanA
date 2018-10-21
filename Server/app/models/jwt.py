from uuid import UUID, uuid4
from typing import Callable

from flask_jwt_extended import create_access_token, create_refresh_token
from mongoengine import *
from werkzeug.exceptions import Unauthorized, Forbidden, UnprocessableEntity

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
        Raises:
            Unauthorized: `identity` is invalid(does not exist in token model due to blacklisted, logged out, etc.)
            Forbidden: 'information of the requester' and the 'information of the token' are inconsistent
            UnprocessableEntity: `identity` can not be parsed as a UUID
        """
        try:
            token = cls.objects(identity=UUID(identity)).first()

            if not token:
                raise Unauthorized('Invalid identity.')

            if token.key.user_agent != user_agent or token.client_ip != remote_addr:
                # token generation 당시의 정보와 대조
                raise Forbidden('You are not token owner.')

            return token

        except ValueError:
            raise UnprocessableEntity('Token identity can not be parsed as a UUID.')


class AccessTokenModel(TokenBase):
    meta = {
        'collection': 'access_token'
    }

    @classmethod
    def create_token(cls, user: UserModel, user_agent: str, remote_addr: str):
        return cls._create_token(create_access_token, user, user_agent, remote_addr)

    @classmethod
    def get_token_with_validation(cls, identity: str, user_agent: str, remote_addr: str):
        return cls._get_token_with_validation(identity, user_agent, remote_addr)


class RefreshTokenModel(TokenBase):
    meta = {
        'collection': 'refresh_token'
    }

    @classmethod
    def create_token(cls, user: UserModel, user_agent: str, remote_addr: str):
        return cls._create_token(create_refresh_token, user, user_agent, remote_addr)

    @classmethod
    def refresh(cls, identity: str, user_agent: str, remote_addr: str):
        token = cls._get_token_with_validation(identity, user_agent, remote_addr)

        return cls.create_token(token.key.owner, user_agent, remote_addr)
