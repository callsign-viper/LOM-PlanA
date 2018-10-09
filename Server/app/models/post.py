from mongoengine import *

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

    @classmethod
    def post(cls, user: UserModel, content: str):
        """
        Creates new post.

        Args:
            user: Instance of UserModel. The context in which this method is called will typically be in the g object.
            content: Content of post. length must between {} and {}.
        """.format(cls.content.min_length, cls.content.max_length)

        return cls(
            owner=user,
            content=content
        ).save()
