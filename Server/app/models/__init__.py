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

    @property
    def created_at_str(self):
        return self.created_at.strftime('%Y-%m-%d %H:%M:%S')

    @property
    def updated_at_str(self):
        return self.updated_at.strftime('%Y-%m-%d %H:%M:%S')

    def save(self, *args, **kwargs):
        self.updated_at = datetime.now()

        return super(Base, self).save(*args, **kwargs)

    def update(self, **kwargs):
        kwargs.update({
            'updated_at': datetime.now()
        })

        return super(Base, self).update(**kwargs)
