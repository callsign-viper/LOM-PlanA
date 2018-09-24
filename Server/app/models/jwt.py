from uuid import UUID, uuid4

from flask import abort
from flask_jwt_extended import create_access_token, create_refresh_token

from app.extensions import mongoengine
from app.models import Base
from app.models.user import UserModel


class TokenBase(Base):
    meta = {
        'abstract': True,
        'allow_inheritance': True
    }

    class Key(mongoengine.EmbeddedDocument):
        owner = mongoengine.ReferenceField(
            document_type=UserModel,
            required=True
        )

        user_agent = mongoengine.StringField(
            required=True
        )

    key = mongoengine.EmbeddedDocumentField(
        document_type=Key,
        primary_key=True
    )
    # 여러 필드를 합쳐 PK로 두기 위함

    client_ip = mongoengine.StringField(
        required=True
    )

    identity = mongoengine.UUIDField(
        unique=True,
        default=uuid4
    )

    @classmethod
    def _create_token(cls, create_token_func, user, user_agent, remote_addr):
        key = cls.Key(owner=user, user_agent=user_agent)
        cls.objects(key=key).delete()

        token = cls(
            key=key,
            client_ip=remote_addr
        ).save()

        identity = token.identity

        return create_token_func(str(identity))

    @classmethod
    def _certify(cls, identity, user_agent, remote_addr):
        try:
            token = cls.objects(identity=UUID(identity)).first()

            if not token:
                abort(401)

            if token.key.user_agent != user_agent or token.client_ip != remote_addr:
                # token generation 당시의 정보와 대조
                abort(403)

            return token

        except ValueError:
            abort(422)


class AccessTokenModel(TokenBase):
    meta = {
        'collection': 'access_token'
    }

    @classmethod
    def create_token(cls, user, user_agent, remote_addr):
        return cls._create_token(create_access_token, user, user_agent, remote_addr)

    @classmethod
    def certify(cls, identity, user_agent, remote_addr):
        return cls._certify(identity, user_agent, remote_addr)


class RefreshTokenModel(TokenBase):
    meta = {
        'collection': 'refresh_token'
    }

    @classmethod
    def create_token(cls, user, user_agent, remote_addr):
        return cls._create_token(create_refresh_token, user, user_agent, remote_addr)

    @classmethod
    def refresh(cls, identity, user_agent, remote_addr):
        token = cls._certify(identity, user_agent, remote_addr)

        return cls.create_token(token.key.owner, user_agent, remote_addr)
