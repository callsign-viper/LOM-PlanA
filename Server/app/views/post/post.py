from flask import g, request
from flask_validation import validate_with_fields
from flask_validation import StringField

from app.models.post import PostModel
from app.views import BaseResource, access_token_required


class Post(BaseResource):
    @validate_with_fields({
        'content': StringField(min_length=PostModel.content.min_length, max_length=PostModel.content.max_length),
    })
    @access_token_required
    def post(self):
        payload = request.json
        content = payload['content']

        post = PostModel.post(g.user, content)

        return {
            'id': str(post.id)
        }, 201
