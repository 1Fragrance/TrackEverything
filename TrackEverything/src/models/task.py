from datetime import datetime
from src import db
from . import STATUS_CHOICES


# Task DB model
class Task(db.Document):
    name = db.StringField(max_length=255, required=True, unique=True)
    description = db.StringField()
    status = db.IntField(choices=STATUS_CHOICES, required=True)
    performer = db.ReferenceField('User', required=False)
    project = db.ReferenceField('Project', required=False)

    start_date = db.DateField(required=True)
    end_date = db.DateField()

    create_date = db.DateTimeField(default=datetime.utcnow, required=True)
    update_date = db.DateTimeField(default=datetime.utcnow, required=True)

    def __init__(self, *args, **kwargs):
        db.Document.__init__(self, *args, **kwargs)

    meta = {
        'collection': 'tasks',
        'ordering': ['-update_date'],
    }
