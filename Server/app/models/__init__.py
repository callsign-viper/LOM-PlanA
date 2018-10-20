from datetime import datetime

from mongoengine import *
from werkzeug.exceptions import BadRequest


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
    def id_str(self):
        return str(self.id)

    @property
    def created_at_str(self):
        return self.created_at.strftime('%Y-%m-%d %H:%M:%S')

    @property
    def updated_at_str(self):
        return self.updated_at.strftime('%Y-%m-%d %H:%M:%S')

    def _validate(self):
        try:
            self.validate()
        except ValidationError as e:
            raise BadRequest('Validation failed - ' + ', '.join(e.to_dict().values()))

    def save(self, *args, **kwargs):
        self.updated_at = datetime.now()

        self._validate()

        return super(Base, self).save(*args, **kwargs)

    def update(self, **kwargs):
        kwargs.update({
            'updated_at': datetime.now()
        })

        self._validate()

        return super(Base, self).update(**kwargs)
