from datetime import datetime
from . import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Employee positions
POSITION_CHOICES = (
    (1, 'None'),
    (2, 'Junior developer'),
    (3, 'Regular developer'),
    (4, 'Senior developer'),
    (5, 'Solution architect'),
    (6, 'Business analyst'),
    (7, 'Project manager'),
    (8, 'Designer'),
    (9, 'Director')
)

# Task/Project statuses
STATUS_CHOICES = (
    (1, 'Not started'),
    (2, 'On work'),
    (3, 'Ended')
)

# User statuses
USER_STATUS_CHOICES = (
    (1, 'Active'),
    (2, 'Banned')
)


# Employee model
class User(db.Document, UserMixin):
    first_name = db.StringField(max_length=255, required=True)
    last_name = db.StringField(max_length=255, required=True)
    patronymic = db.StringField(max_length=255)
    username = db.StringField(max_length=255, required=True, unique=True)
    position = db.IntField(choices=POSITION_CHOICES, required=True)

    tasks = db.ListField(db.ReferenceField('Task'))
    project = db.ReferenceField('Project')

    create_date = db.DateTimeField(default=datetime.utcnow, required=True)
    update_date = db.DateTimeField(default=datetime.utcnow, required=True)

    # Auth
    email = db.EmailField(required=True, unique=True)
    hash_password = db.StringField()
    is_admin = db.BooleanField(default=False)

    # Non-readable property
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        self.hash_password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.hash_password, password)

    def __init__(self, *args, **kwargs):
        db.Document.__init__(self, *args, **kwargs)

    meta = {
        'collection': 'users',
        'ordering': ['-update_date'],
        }


# Override user loading
@login_manager.user_loader
def load_user(user_id):
    user = User.objects(pk=user_id).first()
    if user:
        return user
    return None


# Task model
class Task(db.Document):
    name = db.StringField(max_length=255, required=True, unique=True)
    description = db.StringField()
    status = db.IntField(choices=STATUS_CHOICES)
    performers = db.ListField(db.ReferenceField('User'), required=False)
    project = db.ReferenceField('Project', required=True)
    initiator_person = db.ReferenceField('User')

    start_date = db.DateTimeField()
    end_date = db.DateTimeField()

    create_date = db.DateTimeField(default=datetime.utcnow, required=True)
    update_date = db.DateTimeField(default=datetime.utcnow, required=True)

    def __init__(self, *args, **kwargs):
        db.Document.__init__(self, *args, **kwargs)

    meta = {
        'collection': 'tasks',
        'ordering': ['-update_date'],
        }


# Project model
class Project(db.Document):
    name = db.StringField(max_length=255, required=True, unique=True)
    short_name = db.StringField(max_length=255, required=True, unique=True)
    description = db.StringField()
    status = db.IntField(choices=STATUS_CHOICES, required=True)
    tasks = db.ListField(db.ReferenceField('Task'))
    participants = db.ListField(db.ReferenceField('User'))

    create_date = db.DateTimeField(default=datetime.utcnow, required=True)
    update_date = db.DateTimeField(default=datetime.utcnow, required=True)

    def __init__(self, *args, **kwargs):
        db.Document.__init__(self, *args, **kwargs)

    meta = {
        'collection': 'projects',
        'ordering': ['-update_date'],
        }
