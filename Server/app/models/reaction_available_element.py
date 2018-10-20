from typing import List

from mongoengine import *
from werkzeug.exceptions import BadRequest, Forbidden, NotFound

from app.models import Base
from app.models.user import UserModel


class ReactionAvailableElement(Base):
    meta = {
        'abstract': True,
        'allow_inheritance': True
    }

    owner = ReferenceField(
        document_type=UserModel,
        reverse_delete_rule=DO_NOTHING,
        required=True
    )

    content = StringField(
        required=True,
        min_length=1
    )

    reaction_counts = DictField(
        default={}
    )
    # object마다 reaction model에 접근하면 쿼리 타임이 높아지므로 역정규화

    @property
    def json(self):
        return {
            'id': self.id_str,
            'owner': self.owner.name,
            'content': self.content,
            'reactionInfo': self.reaction_counts,
            'createdAt': self.created_at_str,
            'updatedAt': self.updated_at_str
        }

    def update_(self, requested_user: UserModel, content: str) -> 'ReactionAvailableElement':
        """
        Raises:
            BadRequest: No changed detected in content
            Forbidden: `requested_user` does not have permission to update `post`
        """
        if self.owner != requested_user:
            raise Forbidden('You don\'t have permission to update post {}'.format(self.id))

        if self.content == content:
            raise BadRequest('No changes detected in content.')

        self.update(content=content)

        return self

    def delete_(self, requested_user: UserModel):
        if self.owner != requested_user:
            raise Forbidden('You don\'t have permission to delete post {}'.format(self.id))

        self.delete()


class PostModel(ReactionAvailableElement):
    meta = {
        'collection': 'post'
    }

    @classmethod
    def create(cls, user: UserModel, content: str) -> 'PostModel':
        return cls(
            owner=user,
            content=content
        ).save()

    @classmethod
    def list(cls, user_for_filter: UserModel=None, skip: int=None, size: int=None) -> List['PostModel']:
        if user_for_filter:
            posts = cls.objects(owner=user_for_filter)
        else:
            posts = cls.objects

        return posts[skip:skip + size].order_by('-created_at')

    @classmethod
    def get_by_id(cls, id: str) -> 'PostModel':
        post = cls.objects(id=id).first()

        if not post:
            raise NotFound('Post {} does not exist'.format(id))

        return post

