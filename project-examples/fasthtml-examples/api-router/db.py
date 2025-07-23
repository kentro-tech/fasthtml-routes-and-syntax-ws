from datetime import date,datetime
from fasthtml.common import *

class Project:
    id: int
    name: str
    created: datetime

class Todo:
    id: int
    title: str
    done: bool
    due: date
    project_id: int
    
db = database('todos.db')
db.projects = db.create(Project)
db.todos = db.create(Todo)
