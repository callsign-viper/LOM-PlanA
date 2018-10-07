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

