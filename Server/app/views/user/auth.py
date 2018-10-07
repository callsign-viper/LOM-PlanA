from flask import abort, g, request
from flask_jwt_extended import get_jwt_identity, jwt_refresh_token_required
from flask_validation import validate_common

from app.models.user import UserModel
from app.models.jwt import AccessTokenModel, RefreshTokenModel
from app.views import BaseResource


class Auth(BaseResource):
    @validate_common({'id': str, 'pw': str})
    def post(self):
        payload = request.json

        id = payload['id']
        pw = payload['pw']

        user = UserModel.get_user_as_login(id, pw)

        if not user:
            abort(401, 'Invalid ID or PW.')

        args = [user, g.user_agent, g.remote_addr]

        return {
            'accessToken': AccessTokenModel.create_token(*args),
            'refreshToken': RefreshTokenModel.create_token(*args)
        }


class Refresh(BaseResource):
    @jwt_refresh_token_required
    def get(self):
        return {
            'accessToken': RefreshTokenModel.refresh(get_jwt_identity(), g.user_agent, g.remote_addr)
        }
