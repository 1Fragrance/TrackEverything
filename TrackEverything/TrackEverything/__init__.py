"""
The flask application package.
"""

from flask import Flask, render_template,request,redirect,url_for
from bson import ObjectId
from pymongo import MongoClient
import os

app = Flask(__name__)

title = "TODO sample application with Flask and MongoDB"
heading = "TODO Reminder with Flask and MongoDB"
client = MongoClient("mongodb://127.0.0.1:27017")
db = client.mymongodb
todos = db.todo

import TrackEverything.views

