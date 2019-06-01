# Track Everything structure

This document contain description of application structure.



## Root directory

* documentation - directory which contains all documentation for the application.
* instance - folder with project configuration
* src - directory with application implementation.
* requirements.txt - file that contains all required dependences for running application.
* runserver.py - application start script
* tests.py - script for testing application



## src 

* auth - a package that contains authorization logic of application.
* common - a package that contains constant fields. 
* core - a package that contains application logic. 
* models - a package that contains the classes of all models used in application.
* static/css - application static files.
* templates - a folder containing the template to display the content of web pages
* services - a package that contains special functionality of the project (Machine learning in our case).