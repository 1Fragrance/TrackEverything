from datetime import datetime
from TrackEverything import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

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
class User(UserMixin, db.Document):
    firstname = db.StringField(max_length=255, required=True)
    lastname = db.StringField(max_length=255, required=True)
    patronymic = db.StringField(max_length=255, required=False)
    position = db.StringField(choices=POSITION_CHOICES, required=True)
    tasks = db.ListField(db.ReferenceField('Task'))
    create_date = db.DateTimeField(default=datetime.utcnow, required=True)
    update_date = db.DateTimeField(default=datetime.utcnow, required=True)

    # Auth
    email = db.EmailField(required=True)
    hash_password = db.StringField()

    meta = {
        'collection': 'users',
        'ordering': ['-update_date'],
        }

    # Non-readable property
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


# Task model
class Task(db.Document):
    name = db.StringField(max_length=255, required=True)
    description = db.StringField()
    status = db.StringField(choices=STATUS_CHOICES)
    performers = db.ListField(db.ReferenceField('User'))
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