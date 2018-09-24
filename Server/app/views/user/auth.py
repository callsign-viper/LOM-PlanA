from flask import Response, abort, request
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
        user_agent = request.headers['user_agent']
        remote_addr = request.remote_addr

        user = UserModel.certify(id, pw)

        if not user:
            abort(401)

        args = [user, user_agent, remote_addr]

        return {
            'accessToken': AccessTokenModel.create_token(*args),
            'refreshToken': RefreshTokenModel.create_token(*args)
        }
