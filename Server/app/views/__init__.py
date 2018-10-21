from functools import wraps
import json
import time

from flask import Response, g
from flask_jwt_extended import get_jwt_identity, jwt_required as jwt_required_
from flask_restful import Resource

from app.context import context_property as cp
from app.models.jwt import AccessTokenModel


def jwt_required(fn):
    @wraps(fn)
    @jwt_required_
    def wrapper(*args, **kwargs):
        token = AccessTokenModel.get_token_with_validation(get_jwt_identity(), cp.user_agent, cp.remote_addr)

        g.user = token.key.owner
        # flask_jwt_extended.JWTManager.user_loader_callback_loader 데코레이터를 사용할 수도 있으나,
        # current_user가 LocalProxy로 감싸져서 다루기 힘듬

        return fn(*args, **kwargs)
    return wrapper


class BaseResource(Resource):
    def __init__(self):
        self.now = time.strftime('%Y-%m-%d %H:%M:%S')

    @classmethod
    def unicode_safe_json_dumps(cls, data, status_code=200, **kwargs) -> Response:
        return Response(
            json.dumps(data, ensure_ascii=False),
            status_code,
            content_type='application/json; charset=utf8',
            **kwargs
        )
