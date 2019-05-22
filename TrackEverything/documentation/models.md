# Track Everything Models

This document contains a description for all models used in the application.



## Data Access Models

#### 1. User

Model which contains all information about user

**Fields**: 

* first_name - first name of the user. Can contain from 3 to 255 letters. Required.
* last_name - last name of the user. Can contain from 3 to 255 letters. Required.
* patronymic - patronymic of the user. Can contain from 3 to 255 letters.
* username - user name of the user. Can contain from 3 to 255 letters. Unique in database. Required.
* position - position id  of the user. Required.
* create_date - date when user registered. Required.
* update_date - date when user's information was updated last time. Required.
* project - foreign key to the user project.  
* email - email of the user. Required. Unique in database. Can be used for user's authorization.
* password - user's account password. Can be used for user's authorization.
* status - user status id. Required
* is_admin - flag that separate regular user from admin. Required
  

#### 2. Task

Model which contains all information about task

**Fields**:

* name - name of the task. Can contain from 3 to 255 symbols. Required. Can contain only numbers and letters.
* description - description of the task.
* status - id of task completion status. Required.
* performer - foreign key to the user.
* project - foreign key to the project.
* start_date - date when task starts. Required.
* end_date - date when task ends. Have to be less than start_date.
* create_date - date when task was created. Required.
* update_date - date when task was updated last time. Required.



#### 3. Project

Model which contains all information about project

**Fields:**

* name - name of the project. Can contain from 3 to 255 symbols. Required. Can contain only numbers and letters. Unique in database.
* short_name - short_name of the project. Can contain from 3 to 255 symbols. Required. Can contain only numbers and letters. Unique in database.
* description - description of the project.
* status - project status id. Required.
* create_date - date when project was created. Required.
* update_date - date when project was updated last time. Required.



## Lookups

#### 1. Position_choices

This lookup contains all positions of user.

**Content:**

1. None
2. Junior developer
3. Regular developer
4. Senior developer
5. Solution architect
6. Business analyst
7. Project manager
8. Designer
9. Director



#### 2. Status_choices

This lookup contains all statuses of task or project.

**Content:**

1. Not started
2. On work
3. Ended



#### 3. User_status_choices

This lookup contains all statuses of user's account

**Content:**

1. Active
2. Banned