# Track Everything

Simplify your project management



## About

Track Everything is a web application written in Python Flask. It is a task-tracking application that can help project managers to manage their work on the project with users. Also it can help regular developers to check out tasks which was assigned to them. 



## Features

Client features:

1. User registration system.
2. Browse all projects in the system.
3. Browse all tasks which was assigned to user.
4. Change completion status of the task.
   

Admin features:  

1. Same features as the client.
2. Create, edit and delete projects.
3. Create, edit and delete tasks.
4. Manage users information.
5. Block and restore users accounts. 
     

## Requirements

1. Python3 + Pip

2. MongoDB

   

## Install

1. Clone repository to your local machine

2. Setup local virtual environment

3. Run following command in terminal:

   ``` bash	
   $ pip3 install -r requirements.txt
   ```

   It will install all required dependencies to run application for your virtual environment. After that you can host application on your machine.

    

## Run application

Enter to your virtual environment and  run following command to start using application:

``` bash
$ python runserver.py
```

And follow the link: https://localhost:8000 in your browser



## Tests

Type following to run tests

``` bash
$ python tests.py
```

