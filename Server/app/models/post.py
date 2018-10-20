from typing import List

from mongoengine import *
from werkzeug.exceptions import BadRequest, Forbidden, NotFound

from app.models import Base
from app.models.user import UserModel


class PostModel(Base):
    meta = {
        'collection': 'post'
    }

    owner = ReferenceField(
        document_type=UserModel,
        reverse_delete_rule=DO_NOTHING,
        required=True
    )

    content = StringField(
        required=True,
        min_length=1,
        max_length=3000
    )

    @property
    def json(self):
        return {
            'id': self.id_str,
            'owner': self.owner.name,
            'content': self.content,
            'createdAt': self.created_at_str,
            'updatedAt': self.updated_at_str
        }

    @classmethod
    def post(cls, user: UserModel, content: str) -> 'PostModel':
        """
        Creates new post.

        Args:
            user: Instance of UserModel. The context in which this method is called will typically be in the g object.
            content: Content of post. length must between {} and {}.
        
        Raises:
            BadRequest: content validation failed.
        """.format(cls.content.min_length, cls.content.max_length)

        if not cls.content.min_length < len(content) < cls.content.max_length:
            raise BadRequest('content length must between {} and {}.'.format(
                cls.content.min_length,
                cls.content.max_length
            ))

        return cls(
            owner=user,
            content=content
        ).save()

    @classmethod
    def get_posts(cls, user: 'UserModel'=None, skip: int=None, size: int=None) -> List['PostModel']:
        """
        Get list post.

        Args:
            user: User object for filter
            skip: Number of posts to skip.
            size: Number of posts to retrieve.
        """
        if user:
            posts = cls.objects(owner=user)
        else:
            posts = cls.objects

        return posts[skip:skip + size].order_by('-created_at')

    @classmethod
    def get_post_with_id(cls, id: str) -> 'PostModel':
        """
        Get post object with `id`.

        Args:
            id: ObjectID for post

        Raises:
            NotFound: Post for `id` does not exist
        """
        post = cls.objects(id=id).first()

        if not post:
            raise NotFound('Post {} does not exist'.format(id))

        return post

    @classmethod
    def update_post(cls, post: 'PostModel', requested_user: 'UserModel', content: str) -> 'PostModel':
        """
        Update data of served `post`

        Args:
            post: Post object to update
            requested_user: Requested user usually expressed as g.user
            content: Content of post

        Raises:
            BadRequest: No changed detected in content
            Forbidden: `requested_user` does not have permission to update `post`
        """
        if post.owner != requested_user:
            raise Forbidden('You don\'t have permission to update post {}'.format(post.id))

        if post.content == content:
            raise BadRequest('No changes detected in content.')

        post.update(content=content)

        return post

    @classmethod
    def delete_post(cls, post: 'PostModel', requested_user: 'UserModel'):
        """
        Delete served `post`

        Args:
            post: Post object to delete
            requested_user: Requested user usually expressed as g.user

        Raises:
            Forbidden: `requested_user` does not have permission to delete `post`
        """
        if post.owner != requested_user:
            raise Forbidden('You don\'t have permission to delete post {}'.format(post.id))

        post.delete()
