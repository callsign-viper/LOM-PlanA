from enum import Enum
from typing import List

from mongoengine import *
from werkzeug.exceptions import NotFound

from app.models import Base
from app.models.reaction_available_element import ReactionAvailableElement, CommentModel, PostModel
from app.models.user import UserModel


class ReactionType(Enum):
    GOOD = '1'
    AWESOME = '2'
    SAD = '3'


_REACTION_TARGET_OBJ_TYPE_NAME_MAPPING = {
    CommentModel: 'comment',
    PostModel: 'post'
}


def _get_reaction_target_type(reaction_target_obj: ReactionAvailableElement):
    return _REACTION_TARGET_OBJ_TYPE_NAME_MAPPING[type(reaction_target_obj)]


class ReactionModel(Base):
    meta = {
        'collection': 'reaction'
    }

    class Key(EmbeddedDocument):
        reaction_target_object_id = StringField(
            required=True
        )

        reaction_target_type = StringField(
            required=True
        )

        user = ReferenceField(
            document_type=UserModel,
            reverse_delete_rule=CASCADE,
            required=True
        )

    key = EmbeddedDocumentField(
        document_type=Key,
        primary_key=True
    )

    reaction_type = StringField(
        required=True
    )

    @property
    def json(self):
        key = self.key

        return {
            'owner': key.user.name,
            'reactionType': self.reaction_type
        }

    @classmethod
    def add_new_reaction(cls, reaction_target_obj: ReactionAvailableElement, user: UserModel, reaction_type: ReactionType) -> 'ReactionModel':
        reaction = ReactionModel(
            key=cls.Key(
                reaction_target_oid=reaction_target_obj.id_str,
                reaction_target_type=_get_reaction_target_type(reaction_target_obj),
                user=user
            ),
            reaction_type=reaction_type.value
        ).save()

        reaction_target_obj.reaction_counts[reaction_type.value] += 1
        reaction_target_obj.save()

        return reaction

    @classmethod
    def get_reaction(cls, reaction_target_obj: ReactionAvailableElement, user: UserModel) -> 'ReactionModel':
        reaction = ReactionModel.objects(key=cls.Key(
            reaction_target_oid=reaction_target_obj.id_str,
            reaction_target_type=_get_reaction_target_type(reaction_target_obj),
            user=user
        )).first()

        if not reaction:
            raise NotFound('There\'s no any reaction document.')

        return reaction

    @classmethod
    def get_list_reaction(cls, reaction_target_obj: ReactionAvailableElement, skip: int=None, size: int=None) -> List['ReactionModel']:
        return cls.objects(key=cls.Key(
            reaction_target_oid=reaction_target_obj.id_str,
            reaction_target_type=_get_reaction_target_type(reaction_target_obj)
        ))[skip:skip + size].order_by('-created_at')

    def cancel(self):
        """
        Remove reaction data. There's no any permission check because
        > having a reaction object(self) means that requester have already authenticated via `key`.
        """

        post = self.key.create
        post.reaction_counts[self.reaction_type] -= 1
        post.save()

        self.delete()
