# Track Everything: Requirements

Track Everything - it is a task-tracking application which should help people to organize work on projects.



## What problem this application should solve?

Nowadays, time is one of the most expensive resources. It means that modern companies are needed in applications which can help them to organize their production. It will help companies not to waste time on things that can be done more quickly and easily that they doing now. I think that task tracking application should help them to save some time on project organization and automate the production.



## Analogs 

There are a lot of task-tracking applications on the Internet. Next will be comparison between some of them with cons and pros.



#### 1. Wunderlist

##### Pros:

* Add own tags for tasks.
* Print own dashboard
* Browse closed tasks
* Hotkeys.
* Chrome extension
* Can undo any deleting operation

**Cons**:

* Uncomfortable interface
  

### 2. Todoist

At first glance it looks simple task tracking service without any new features.

**Pros:**

* Compact
* Opportunity to choose theme
* Quick search
* Activity log
* Opportunity to plan next week
* Filters
* Creating own template task.
* Achievements system

**Cons:**

* In the free version, many features are limited
* Uncomfortable interface



### 3. Any.do

**Pros:**

* Comfortable and beautiful interface

* Supports cloud storages
* Opportunity to create subtasks

**Cons:** 

* No tags
* No text search
* No offline version



#### 4. TickTick

**Pros**:

* Tutorial after registration
* Opportunity to add task using callendar
* Statistic
* Mobile version
* Supports Siri



### 5. Jira

One of the most popular task tracking service.

**Pros:**

* Easy to use
* A lot of filters
* Opportunity to view various graphs, reports, charts with useful information

**Cons:**

* 1 task = 1 performer



## Summarizing

Now, it is possible to determine what features are main in task tracking application.

1. Authorization
2. Add, edit and delete task
3. Add, edit and delete projects
4. Browse assigned tasks
5. Browse projects
6. User managing system
7. Task statuses
8. Separation between client and admin



## Logical architecture

Application will contain 3 main logical structures:

1. User
2. Task
3. Project 



#### User  

User is the main object in application. Every operation will be done by user for user.
Will contain inside:

* Reference on project
* Auth information
* Personal information
* Position on the project.
  

#### Task

Task is object which we can assign to user.

Will contain inside:

* Task description
* Start date
* End date
* Reference on performer
* Status of completion
* Reference on project
* 

#### Project

Project is object which links task and users with each other.

Will contain inside:

* Project description
* Status