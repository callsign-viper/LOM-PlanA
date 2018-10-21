from flask import Response, abort, request
from flask_validation import json_required, validate_with_fields
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
    @json_required
    @validate_with_fields({
        'id': StringField(min_length=UserModel.id.min_length, max_length=UserModel.id.max_length),
        'pw': StringField(min_length=8),
        'email': StringField(regex=email_regex),
        'name': StringField(min_length=UserModel.name.min_length, max_length=UserModel.name.max_length),
        'nickname': StringField(required=False, min_length=UserModel.nickname.min_length, max_length=UserModel.nickname.max_length),
        'bio': StringField(required=False, min_length=UserModel.bio.min_length, max_length=UserModel.bio.max_length)
    })
    def post(self):
        payload = request.json
        id = payload['id']
        pw = payload['pw']
        email = payload['email']
        name = payload['name']
        nickname = payload.get('nickname')
        bio = payload.get('bio')

        UserModel.signup(id, pw, email, name, nickname, bio)

        return Response('', 201)
