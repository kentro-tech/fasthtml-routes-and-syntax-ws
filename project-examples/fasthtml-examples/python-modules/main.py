from fasthtml.common import *
from datetime import datetime
from monsterui.all import *
from db import db, Project, Todo
from components.cards import TodoCard
from components.forms import mk_todo_form
from pages import ProjectTodosPage, ProjectPage, mk_todo_list, mk_project_list
app, rt = fast_app(hdrs=Theme.slate.headers())

def tid(id): return f'todo-{id}'

@app.delete
async def delete_todo(id:int):
    "Delete if it exists, if not someone else already deleted it so no action needed"
    try: db.todos.delete(id)
    except NotFoundError: pass

@rt
async def index():
    "Main page showing all projects"
    return ProjectPage(db.projects())

@rt
async def create_project(name: str):
    if name.strip():
        db.projects.insert(Project(name=name.strip(), created=datetime.now()))
    return mk_project_list(db.projects())

@rt('/project/{project_id}')
async def project_todos(project_id: int):
    "Todo list for a specific project"
    project = db.projects[project_id]
    todos_list = db.todos(where=f'project_id={project_id}', order_by='due')
    return ProjectTodosPage(project.name, project_id, todos_list)

@rt 
async def upsert_todo(todo:Todo):
    if todo.title.strip(): db.todos.insert(todo,replace=True)
    todos_list = db.todos(where=f'project_id={todo.project_id}', order_by='due')
    return mk_todo_list(todo.project_id, todos_list),mk_todo_form(todo.project_id)(hx_swap_oob='true',hx_target='#todo-input',hx_swap='outerHTML')

@rt 
async def toggle_done(id:int):
    "Reverses done boolean in the database and returns the todo (rendered with __ft__)"
    existing = db.todos[id]
    updated = db.todos.update({
        'id': id,
        'done': not existing.done,
        'title': existing.title,
        'due': existing.due,
        'project_id': existing.project_id
    })
    return TodoCard(updated.due, updated.done, updated.title, updated.id)


@rt 
async def edit_todo(id:int): 
    todo = db.todos[id]
    return Card(mk_todo_form(todo.project_id, todo, btn_text="Save"))

serve(port=5003)
