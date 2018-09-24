from flask import Response, abort, request
from flask_validation import validate_with_fields
from flask_validation import StringField
from flask_validation.common_regex import email as email_regex

from app.models.user import UserModel
from app.views import BaseResource


class CheckIDIsAvailable(BaseResource):
    def get(self, id):
        if UserModel.is_id_exist(id):
            abort(409)
        else:
            return Response('', 200)


class CheckEmailIsAvailable(BaseResource):
    def get(self, email):
        if UserModel.is_email_exist(email):
            abort(409)
        else:
            return Response('', 200)


class Signup(BaseResource):
    @validate_with_fields({
        'id': StringField(min_length=4, max_length=50),
        'pw': StringField(),
        'email': StringField(regex=email_regex),
        'name': StringField(min_length=2, max_length=16),
        'nickname': StringField(required=False, min_length=1, max_length=30),
        'bio': StringField(required=False, min_length=1, max_length=85)
    })
    def post(self):
        payload = request.json
        id = payload['id']
        pw = payload['pw']
        email = payload['email']
        name = payload['name']
        nickname = payload.get('nickname')
        bio = payload.get('bio')

        res = UserModel.signup(id, pw, email, name, nickname, bio)

        if not res:
            abort(409)

        return Response('', 201)
