"""
Single-file Air application example.
A complete todo/project management app in one file.

Run with: python main.py
Then visit: http://localhost:8000
"""

import air
from datetime import date, datetime
from typing import Optional
import sqlite3
import os
from fastapi import Form

app = air.Air()

# Simple database setup
DB_FILE = "todos.db"

def init_db():
    """Initialize the database with required tables."""
    conn = sqlite3.connect(DB_FILE)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            created TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done INTEGER DEFAULT 0,
            due TEXT NOT NULL,
            project_id INTEGER NOT NULL,
            FOREIGN KEY (project_id) REFERENCES projects (id)
        )
    """)
    conn.commit()
    conn.close()

def get_projects():
    """Get all projects."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.execute("SELECT id, name, created FROM projects ORDER BY created DESC")
    projects = [{"id": row[0], "name": row[1], "created": row[2]} for row in cursor.fetchall()]
    conn.close()
    return projects

def get_project(project_id: int):
    """Get a single project by ID."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.execute("SELECT id, name, created FROM projects WHERE id = ?", (project_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"id": row[0], "name": row[1], "created": row[2]}
    return None

def create_project(name: str):
    """Create a new project."""
    conn = sqlite3.connect(DB_FILE)
    conn.execute("INSERT INTO projects (name, created) VALUES (?, ?)", 
                 (name, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_todos(project_id: int):
    """Get todos for a project."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.execute("""
        SELECT id, title, done, due, project_id 
        FROM todos 
        WHERE project_id = ? 
        ORDER BY due, id
    """, (project_id,))
    todos = [{"id": row[0], "title": row[1], "done": bool(row[2]), 
              "due": row[3], "project_id": row[4]} for row in cursor.fetchall()]
    conn.close()
    return todos

def get_todo(todo_id: int):
    """Get a single todo by ID."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.execute("SELECT id, title, done, due, project_id FROM todos WHERE id = ?", (todo_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"id": row[0], "title": row[1], "done": bool(row[2]), 
                "due": row[3], "project_id": row[4]}
    return None

def create_todo(title: str, due: str, project_id: int):
    """Create a new todo."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.execute("""
        INSERT INTO todos (title, done, due, project_id) 
        VALUES (?, 0, ?, ?)
    """, (title, due, project_id))
    todo_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return todo_id

def update_todo(todo_id: int, title: str = None, done: bool = None, due: str = None):
    """Update a todo."""
    conn = sqlite3.connect(DB_FILE)
    if title is not None:
        conn.execute("UPDATE todos SET title = ? WHERE id = ?", (title, todo_id))
    if done is not None:
        conn.execute("UPDATE todos SET done = ? WHERE id = ?", (int(done), todo_id))
    if due is not None:
        conn.execute("UPDATE todos SET due = ? WHERE id = ?", (due, todo_id))
    conn.commit()
    conn.close()

def delete_todo(todo_id: int):
    """Delete a todo."""
    conn = sqlite3.connect(DB_FILE)
    conn.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
    conn.commit()
    conn.close()

# Utility functions
def tid(todo_id): 
    return f'todo-{todo_id}'

def is_overdue(due_date_str: str) -> bool:
    """Check if a due date is overdue."""
    try:
        due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
        return date.today() > due_date
    except:
        return False

# Components
def TodoCard(todo):
    """Render a todo card with edit/delete actions."""
    due_style = "color: red; font-weight: bold;" if is_overdue(todo["due"]) else ""
    done_style = "text-decoration: line-through; opacity: 0.7;" if todo["done"] else ""
    
    return air.Div(
        air.Div(
            air.Input(
                type="checkbox", 
                checked=todo["done"],
                hx_post=f"/toggle/{todo['id']}",
                hx_target=f"#{tid(todo['id'])}",
                hx_swap="outerHTML"
            ),
            air.Span(todo["title"], style=done_style),
            style="display: flex; align-items: center; gap: 10px; margin-bottom: 5px;"
        ),
        air.Div(
            air.Small(f"Due: {todo['due']}", style=due_style),
            air.Div(
                air.Button(
                    "Edit", 
                    hx_get=f"/edit/{todo['id']}", 
                    hx_target=f"#{tid(todo['id'])}",
                    hx_swap="outerHTML",
                    style="margin-right: 5px; padding: 2px 8px; font-size: 12px;"
                ),
                air.Button(
                    "Delete", 
                    hx_delete=f"/delete/{todo['id']}", 
                    hx_target=f"#{tid(todo['id'])}",
                    hx_swap="outerHTML",
                    style="padding: 2px 8px; font-size: 12px; background: #dc3545; color: white; border: none;"
                ),
                style="margin-top: 5px;"
            ),
            style="display: flex; justify-content: space-between; align-items: center;"
        ),
        id=tid(todo['id']),
        style="border: 1px solid #ddd; padding: 10px; margin-bottom: 10px; border-radius: 5px; background: #f9f9f9;"
    )

def ProjectCard(project):
    """Render a project card."""
    created_date = datetime.fromisoformat(project["created"]).strftime('%Y-%m-%d')
    return air.Div(
        air.H3(
            air.A(project["name"], href=f'/project/{project["id"]}', style="text-decoration: none; color: #007bff;")
        ),
        air.P(f"Created: {created_date}", style="color: #666; margin: 5px 0;"),
        id=f'project-{project["id"]}',
        style="border: 1px solid #ddd; padding: 15px; margin-bottom: 15px; border-radius: 5px; background: #f8f9fa;"
    )

def mk_project_form():
    """Create project form."""
    return air.Form(
        air.Div(
            air.Input(
                name='name', 
                placeholder='New Project Name',
                required=True,
                style="padding: 8px; margin-right: 10px; border: 1px solid #ddd; border-radius: 3px;"
            ),
            air.Button(
                'Create Project',
                type="submit",
                style="padding: 8px 15px; background: #007bff; color: white; border: none; border-radius: 3px; cursor: pointer;"
            ),
            style="display: flex; align-items: center; margin-bottom: 20px;"
        ),
        hx_post='/create_project',
        hx_target='#project-list',
        hx_swap='innerHTML',
        id='project-input'
    )

def mk_todo_form(project_id: int, todo=None, btn_text="Add Todo"):
    """Create todo form."""
    if todo is None:
        todo = {"title": "", "due": date.today().isoformat(), "id": None}
    
    inputs = [
        air.Input(
            name='title', 
            value=todo["title"], 
            placeholder='Todo title',
            required=True,
            style="padding: 8px; margin-right: 10px; border: 1px solid #ddd; border-radius: 3px; flex-grow: 1;"
        ),
        air.Input(
            name='due', 
            value=todo["due"], 
            type="date",
            style="padding: 8px; margin-right: 10px; border: 1px solid #ddd; border-radius: 3px;"
        ),
        air.Input(name='project_id', value=project_id, type="hidden")
    ]
    
    if todo["id"]: 
        inputs.append(air.Input(name='id', value=todo["id"], type="hidden"))
        
    return air.Form(
        air.Div(
            *inputs,
            air.Button(
                btn_text,
                type="submit",
                style="padding: 8px 15px; background: #28a745; color: white; border: none; border-radius: 3px; cursor: pointer;"
            ),
            style="display: flex; align-items: center; margin-bottom: 20px;"
        ),
        hx_post='/upsert_todo',
        hx_target='#todo-list',
        hx_swap='innerHTML',
        id='todo-input'
    )

def mk_todo_list(project_id: int):
    """Create todo list."""
    todos = get_todos(project_id)
    if not todos:
        return air.Div(
            air.P("No todos yet. Add one above!", style="color: #666; font-style: italic;"),
            id='todo-list'
        )
    
    return air.Div(
        *[TodoCard(todo) for todo in todos],
        id='todo-list'
    )

def mk_project_list():
    """Create project list."""
    projects = get_projects()
    if not projects:
        return air.Div(
            air.P("No projects yet. Create one above!", style="color: #666; font-style: italic;"),
            id='project-list'
        )
    
    return air.Div(
        *[ProjectCard(project) for project in projects],
        id='project-list'
    )

# Routes
@app.get("/")
async def index():
    """Main page showing all projects."""
    return air.Html(
        air.Head(
            air.Title("Todo Projects - Single File Example"),
            air.Script(src="https://unpkg.com/htmx.org@1.9.10"),
            air.Style("""
                body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
                h1 { color: #333; }
                .container { margin: 20px 0; }
                a { color: #007bff; text-decoration: none; }
                a:hover { text-decoration: underline; }
            """)
        ),
        air.Body(
            air.H1("📋 Todo Projects"),
            air.P("Manage your projects and todos in this single-file Air application."),
            mk_project_form(),
            mk_project_list()
        )
    )

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
    
    return air.Html(
        air.Head(
            air.Title(f"{project['name']} - Todos"),
            air.Script(src="https://unpkg.com/htmx.org@1.9.10"),
            air.Style("""
                body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
                h1 { color: #333; }
                .back-link { display: inline-block; margin-bottom: 20px; }
                a { color: #007bff; text-decoration: none; }
                a:hover { text-decoration: underline; }
            """)
        ),
        air.Body(
            air.A("← Back to Projects", href="/", class_="back-link"),
            air.H1(f"📝 {project['name']} - Todos"),
            mk_todo_form(project_id),
            mk_todo_list(project_id)
        )
    )

@app.post("/upsert_todo")
async def upsert_todo(
    title: str = Form(...), 
    due: str = Form(...), 
    project_id: int = Form(...), 
    id: Optional[int] = Form(None)
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
        todo = get_todo(todo_id)
        return TodoCard(todo)
    return ""

@app.delete("/delete/{todo_id}")
async def delete_todo_route(todo_id: int):
    """Delete a todo."""
    delete_todo(todo_id)
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

# Initialize database and run
if __name__ == "__main__":
    # Initialize database
    init_db()
    
    # Add some sample data if database is empty
    if not get_projects():
        create_project("Sample Project")
        project_id = 1  # First project will have ID 1
        create_todo("Learn Air framework", date.today().isoformat(), project_id)
        create_todo("Build something awesome", (date.today()).isoformat(), project_id)
    
    print("🚀 Starting Air single-file example...")
    print("📂 Database: todos.db")
    print("🌐 Visit: http://localhost:8000")
    
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
