import os
from flask import Flask, render_template,request,redirect,url_for
from bson import ObjectId
from pymongo import MongoClient
from TrackEverything.models import db, Project, Task, Employee

app = Flask(__name__)

## include db name in URI; _HOST entry overwrites all others
app.config['MONGODB_HOST'] = 'mongodb://localhost:27017/sivji-sandbox'
app.debug = True

db.init_app(app)

import TrackEverything.views

