from datetime import datetime
from src import db
from . import STATUS_CHOICES


# Project DB model
class Project(db.Document):
    name = db.StringField(max_length=255, required=True, unique=True)
    short_name = db.StringField(max_length=255, required=True, unique=True)
    description = db.StringField()
    status = db.IntField(choices=STATUS_CHOICES, required=True)

    create_date = db.DateTimeField(default=datetime.utcnow, required=True)
    update_date = db.DateTimeField(default=datetime.utcnow, required=True)


    def __init__(self, *args, **kwargs):
        db.Document.__init__(self, *args, **kwargs)

    meta = {
        'collection': 'projects',
        'ordering': ['-update_date'],
    }
