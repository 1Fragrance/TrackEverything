from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from src import db, login_manager

from . import POSITION_CHOICES, USER_STATUS_CHOICES


# User DB model
class User(db.Document, UserMixin):
    first_name = db.StringField(max_length=255, required=True)
    last_name = db.StringField(max_length=255, required=True)
    patronymic = db.StringField(max_length=255)
    username = db.StringField(max_length=255, required=True, unique=True)
    position = db.IntField(choices=POSITION_CHOICES, required=True)
    create_date = db.DateTimeField(default=datetime.utcnow, required=True)
    update_date = db.DateTimeField(default=datetime.utcnow, required=True)
    project = db.ReferenceField('Project')

    # Auth
    email = db.EmailField(required=True, unique=True)
    hash_password = db.StringField()
    status = db.IntField(choices=USER_STATUS_CHOICES, required=True)
    is_admin = db.BooleanField(default=False, required=True)

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
