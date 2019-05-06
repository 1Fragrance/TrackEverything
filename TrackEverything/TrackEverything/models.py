from flask_mongoengine import MongoEngine
from datetime import datetime

db = MongoEngine()

# Employee positions
POSITION_CHOICES = (
    (0, 'None'),
    (1, 'Junior developer'),
    (2, 'Regular developer'),
    (3, 'Senior developer'),
    (4, 'Solution architector'),
    (5, 'Business analyst'),
    (6, 'Project manager'),
    (7, 'Designer'),
    (8, 'Director')
)

# Task/Project statuses
STATUS_CHOICES = (
    (0, 'Not started'),
    (1, 'On work'),
    (2, 'Ended')
)


# Employee model
class Employee(db.Document):
    firstname = db.StringField(max_length=255, required=True)
    lastname = db.StringField(max_length=255, required=True)
    patronymic = db.StringField(max_length=255, required=False)
    email = db.EmailField(required=True)
    position = db.StringField(choices=POSITION_CHOICES, required=True)
    tasks = db.ListField(db.ReferenceField('Task'))

    create_date = db.DateTimeField(default=datetime.utcnow, required=True)
    update_date = db.DateTimeField(default=datetime.utcnow, required=True)
    
    meta = {
        'collection': 'employees',
        'ordering': ['-update_date'],
        }

# Task model
class Task(db.Document):
    name = db.StringField(max_length=255, required=True)
    description = db.StringField()
    status = db.StringField(choices=STATUS_CHOICES)
    performers = db.ListField(db.ReferenceField('Employee'))
    project = db.ReferenceField('Project')

    start_date = db.DateTimeField()
    end_date = db.DateTimeField()
    create_date = db.DateTimeField(default=datetime.utcnow, required=True)
    update_date = db.DateTimeField(default=datetime.utcnow, required=True)

    meta = {
        'collection': 'tasks',
        'ordering': ['-update_date'],
        }

# Project model
class Project(db.Document):
    name = db.StringField(max_length=255, required=True)
    shortname = db.StringField(max_length=255, required=True)
    description = db.StringField()
    status = db.StringField(choices=STATUS_CHOICES, required=True)
    tasks = db.ListField(db.ReferenceField('Task'))

    create_date = db.DateTimeField(default=datetime.utcnow, required=True)
    update_date = db.DateTimeField(default=datetime.utcnow, required=True)

    meta = {
        'collection': 'projects',
        'ordering': ['-update_date'],
        }