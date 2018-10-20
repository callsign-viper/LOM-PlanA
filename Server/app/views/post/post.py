from flask import current_app, g, request
from flask_validation import validate_with_fields
from flask_validation import StringField

from app.models.post import PostModel
from app.views import BaseResource, access_token_required

_POST_CONTENT_TERM = StringField(min_length=PostModel.content.min_length, max_length=PostModel.content.max_length)


class Post(BaseResource):
    @validate_with_fields({
        'content': _POST_CONTENT_TERM,
    })
    @access_token_required
    def post(self):
        payload = request.json
        content = payload['content']

        post = PostModel.post(g.user, content)

        return {
            'id': str(post.id)
        }, 201

    def get(self):
        post_retrieve_config = current_app.config['POST_RETRIEVE_CONFIG']
        default_size = post_retrieve_config['default_size']
        default_skip = post_retrieve_config['default_skip']
        # default_size, default_skip = post_retrieve_config.values()도 가능하지만, 불필요하며 결합도만 늘어남

        size = int(request.args.get('size', default_size))
        skip = int(request.args.get('skip', default_skip))

        return [{
            'id': str(post.id),
            'owner': post.owner.name,
            'content': post.content,
            'createdAt': post.created_at_str,
            'updatedAt': post.updated_at_str
        } for post in PostModel.get_posts(size, skip)]


class PostItem(BaseResource):
    @validate_with_fields({
        'content': _POST_CONTENT_TERM,
    })
    @access_token_required
    def patch(self, id):
        post = PostModel.get_post_with_id(id)

        payload = request.json
        content = payload['content']

        PostModel.update_post(post, g.user, content)

        return

    @access_token_required
    def delete(self, id):
        post = PostModel.get_post_with_id(id)

        PostModel.delete_post(post, g.user)

        return
