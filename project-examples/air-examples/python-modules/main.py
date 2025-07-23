"""
Python modules Air application example.
A todo/project management app organized into logical modules.

Run with: python main.py
Then visit: http://localhost:8001
"""

import air
from datetime import datetime
from fastapi import Form
from db import get_projects, get_project, create_project, get_todos
from components.cards import TodoCard, ProjectCard
from components.forms import mk_todo_form, mk_project_form
from pages import ProjectPage, ProjectTodosPage, mk_todo_list, mk_project_list
from db import init_db, get_todo, create_todo, update_todo, delete_todo

app = air.Air()

@app.delete("/delete/{todo_id}")
async def delete_todo_route(todo_id: int):
    """Delete a todo."""
    delete_todo(todo_id)
    return ""

@app.get("/")
async def index():
    """Main page showing all projects."""
    projects = get_projects()
    return ProjectPage(projects)

@app.post("/create_project")
async def create_project_route(name: str = Form(...)):
    """Create a new project."""
    if name.strip():
        create_project(name.strip())
    return mk_project_list()

@app.get("/project/{project_id}")
async def project_todos(project_id: int):
    """Todo list for a specific project."""
    project = get_project(project_id)
    if not project:
        return air.Html(
            air.Head(air.Title("Project Not Found")),
            air.Body(
                air.H1("Project Not Found"),
                air.P(air.A("← Back to Projects", href="/"))
            )
        )
    
    todos_list = get_todos(project_id)
    return ProjectTodosPage(project["name"], project_id, todos_list)

@app.post("/upsert_todo") 
async def upsert_todo(
    title: str = Form(...), 
    due: str = Form(...), 
    project_id: int = Form(...), 
    id: int = Form(None)
):
    """Create or update a todo."""
    if title.strip():
        if id:
            update_todo(id, title=title.strip(), due=due)
        else:
            create_todo(title.strip(), due, project_id)
    return mk_todo_list(project_id)

@app.post("/toggle/{todo_id}")
async def toggle_done(todo_id: int):
    """Toggle todo done status."""
    todo = get_todo(todo_id)
    if todo:
        update_todo(todo_id, done=not todo["done"])
        updated_todo = get_todo(todo_id)
        return TodoCard(updated_todo)
    return ""

@app.get("/edit/{todo_id}")
async def edit_todo(todo_id: int): 
    """Show edit form for a todo."""
    todo = get_todo(todo_id)
    if todo:
        return air.Div(
            mk_todo_form(todo["project_id"], todo, btn_text="Save"),
            style="border: 2px solid #007bff; padding: 10px; border-radius: 5px; background: #f0f8ff;"
        )
    return ""

if __name__ == "__main__":
    # Initialize database
    init_db()
    
    # Add some sample data if database is empty
    if not get_projects():
        create_project("Sample Project")
        project_id = 1  # First project will have ID 1
        from datetime import date
        create_todo("Learn Air framework", date.today().isoformat(), project_id)
        create_todo("Build modular app", date.today().isoformat(), project_id)
    
    print("🚀 Starting Air python-modules example...")
    print("📂 Database: todos.db")
    print("🌐 Visit: http://localhost:8001")
    
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
