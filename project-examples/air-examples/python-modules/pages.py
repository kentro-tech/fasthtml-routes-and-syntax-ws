"""
Page layouts and high-level components.
Complete page templates for the Air python-modules example.
"""

import air
from components.cards import TodoCard, ProjectCard
from components.forms import mk_todo_form, mk_project_form
from db import get_projects

def mk_todo_list(project_id: int):
    """Create todo list for a project."""
    from db import get_todos
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

def ProjectPage(projects):
    """Main projects page layout."""
    return air.Html(
        air.Head(
            air.Title("Todo Projects - Python Modules Example"),
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
            air.P("This example demonstrates organizing Air code into logical modules."),
            air.Small("📁 Check out: db.py, components/, pages.py, and main.py", style="color: #666;"),
            mk_project_form(),
            mk_project_list()
        )
    )

def ProjectTodosPage(project_name: str, project_id: int, todos_list):
    """Project todos page layout."""
    return air.Html(
        air.Head(
            air.Title(f"{project_name} - Todos"),
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
            air.H1(f"📝 {project_name} - Todos"),
            air.P("Manage todos for this project.", style="color: #666;"),
            mk_todo_form(project_id),
            mk_todo_list(project_id)
        )
    )
