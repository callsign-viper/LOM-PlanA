from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_refresh_token_required
from flask_validation import json_required, validate_common

from app.context import context_property as cp
from app.models.user import UserModel
from app.models.jwt import AccessTokenModel, RefreshTokenModel
from app.views import BaseResource


class Auth(BaseResource):
    @json_required
    @validate_common({'id': str, 'pw': str})
    def post(self):
        payload = request.json

        id = payload['id']
        pw = payload['pw']

        user = UserModel.get_user_as_login(id, pw)

        create_token_args = [user, cp.user_agent, cp.remote_addr]

        return {
            'accessToken': AccessTokenModel.create_token(*create_token_args),
            'refreshToken': RefreshTokenModel.create_token(*create_token_args)
        }


class Refresh(BaseResource):
    @jwt_refresh_token_required
    def get(self):
        return {
            'accessToken': RefreshTokenModel.refresh(get_jwt_identity(), cp.user_agent, cp.remote_addr)
        }
