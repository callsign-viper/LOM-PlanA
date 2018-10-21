from flask import current_app, request
from flask_validation import json_required, validate_with_fields
from flask_validation import StringField

from app.context import context_property as cp
from app.models.reaction_available_element import PostModel
from app.views import BaseResource, jwt_required

_POST_CONTENT_TERM = StringField(min_length=PostModel.content.min_length)


class Post(BaseResource):
    @validate_with_fields({
        'content': _POST_CONTENT_TERM,
    })
    @json_required
    @jwt_required
    def post(self):
        payload = request.json
        content = payload['content']

        post = PostModel.create(cp.requested_user_obj, content)

        return {
            'id': str(post.id)
        }, 201

    def get(self):
        skip = int(request.args.get('skip', cp.post_list_default_skip))
        size = int(request.args.get('size', cp.post_list_default_size))

        return [post.json for post in PostModel.list(skip=skip, size=size)]


class PostItem(BaseResource):
    @validate_with_fields({
        'content': _POST_CONTENT_TERM,
    })
    @json_required
    @jwt_required
    def patch(self, id):
        post = PostModel.get_by_id(id)

        payload = request.json
        content = payload['content']

        post.update_(cp.requested_user_obj, content)

        return

    @jwt_required
    def delete(self, id):
        post = PostModel.get_by_id(id)

        post.delete_(cp.requested_user_obj)

        return
