# to-do-app-backend

## Prerequisites

Python 3, PostgreSQL (or some other database)

## Installation

1. Clone project
2. Install packages
3. Create a database (default name: 'todo')
4. Set database URI (app.py line 8). For PostgreSQL - 'postgresql://db_user:password@localhost:port/db_name'
5. Set up the database  
`cd project_directory`  
   `python`  
   `>>> from app import db`  
   `>>> db.create_all()`  
   `>>> exit()`  
6. Start project `python app.py`

## Unit testing

`python test.py`
