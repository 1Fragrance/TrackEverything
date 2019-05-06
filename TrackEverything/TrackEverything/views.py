from datetime import datetime
from flask import render_template
from TrackEverything import app

@app.route('/', methods=['GET'])
def index():
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

# Project api
@app.route('/project', methods=['GET'])
def get_projects():
    pass

@app.route('/project/<int:id>', methods=['GET'])
def get_project(id):
    pass

@app.route('/project/<int:id>', methods=['POST'])
def create_project(id):
    pass

@app.route('/project/<int:id>', methods=['PUT'])
def edit_project(id):
    pass

@app.route('/project/<int:id>', methods=['DELETE'])
def delete_project(id):
    pass

# Emplyee api
@app.route('/employee', methods=['GET'])
def get_employees():
    pass

@app.route('/employee/<int:id>', methods=['GET'])
def get_employee(id):
    pass

@app.route('/employee/<int:id>', methods=['POST'])
def create_empolyee(id):
    pass

@app.route('/employee/<int:id>', methods=['PUT'])
def edit_employee(id):
    pass

@app.route('/employee/<int:id>', methods=['DELETE'])
def delete_emplyee(id):
    pass

# Task api
@app.route('/task', methods=['GET'])
def get_tasks():
    pass

@app.route('/task/<int:id>', methods=['GET'])
def get_task(id):
    pass

@app.route('/task/<int:id>', methods=['POST'])
def create_task(id):
    pass

@app.route('/task/<int:id>', methods=['PUT'])
def edit_task(id):
    pass

@app.route('/task/<int:id>', methods=['DELETE'])
def delete_task(id):
    pass

# Auth api
@app.route('/login', methods=['POST', 'GET'])
def login():
    pass

@app.route('/logout')
def logout():
    pass