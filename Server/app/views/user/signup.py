from flask import Response, abort, request
from flask_validation import validate_with_fields
from flask_validation import StringField

from app.models.user import UserModel
from app.views import BaseResource


class CheckIDIsAvailable(BaseResource):
    def get(self, id):
        if UserModel.is_id_exist(id):
            abort(409)
        else:
            return Response('', 200)


class Signup(BaseResource):
    @validate_with_fields({
        'id': StringField(min_length=4, max_length=50),
        'pw': StringField(),
        'name': StringField(min_length=2, max_length=16),
        'nickname': StringField(required=False, min_length=1, max_length=30),
        'bio': StringField(required=False, min_length=1, max_length=85)
    })
    def post(self):
        payload = request.json
        id = payload['id']
        pw = payload['pw']
        name = payload['name']
        nickname = payload.get('nickname')
        bio = payload.get('bio')

        if UserModel.is_id_exist(id):
            abort(409)

        UserModel.signup(id, pw, name, nickname, bio)

        return Response('', 201)
