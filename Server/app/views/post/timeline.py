from flask import abort, current_app, request

from app.models.reaction_available_element import PostModel
from app.models.user import UserModel
from app.views import BaseResource


class Timeline(BaseResource):
    def get(self, id):
        user = UserModel.objects(id=id).first()

        if not user:
            abort(404, 'Unknown user ID.')

        post_retrieve_config = current_app.config['POST_RETRIEVE_CONFIG']
        default_skip = post_retrieve_config['default_skip']
        default_size = post_retrieve_config['default_size']

        skip = int(request.args.get('skip', default_skip))
        size = int(request.args.get('size', default_size))

        return [post.json for post in PostModel.list(user, skip, size)]
