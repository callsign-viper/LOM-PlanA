from datetime import datetime

from mongoengine import *


class Base(Document):
    meta = {
        'abstract': True,
        'allow_inheritance': True
    }

    created_at = DateTimeField(
        default=datetime.now
    )

    updated_at = DateTimeField(
        default=datetime.now
    )

    def save(self, *args, **kwargs):
        self.updated_at = datetime.now()

        return super(Base, self).save(*args, **kwargs)
