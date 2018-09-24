from datetime import datetime

from app.extensions import mongoengine


class Base(mongoengine.Document):
    meta = {
        'abstract': True,
        'allow_inheritance': True
    }

    created_at = mongoengine.DateTimeField(
        default=datetime.now
    )

    updated_at = mongoengine.DateTimeField(
        default=datetime.now
    )

    def save(self, *args, **kwargs):
        self.updated_at = datetime.now()

        super(Base, self).save(*args, **kwargs)
