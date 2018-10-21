from flask import request

from app.context import context_property as cp
from app.models.reaction_available_element import PostModel
from app.models.user import UserModel
from app.views import BaseResource


class Timeline(BaseResource):
    def get(self, id):
        user = UserModel.objects(id=id).first()

        skip = int(request.args.get('skip', cp.post_list_default_skip))
        size = int(request.args.get('size', cp.post_list_default_size))

        return [post.json for post in PostModel.list(user, skip, size)]
