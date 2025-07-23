"""
Todo routes using the global app instance.
All todo-related routes and components.
"""

import air
from datetime import date, datetime
from fastapi import Form
from globals import app, get_project, get_todos, get_todo, create_todo, update_todo, delete_todo

def tid(todo_id):
    """Generate todo element ID."""
    return f'todo-{todo_id}'

def is_overdue(due_date_str: str) -> bool:
    """Check if a due date is overdue."""
    try:
        due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
        return date.today() > due_date
    except:
        return False

def TodoCard(todo):
    """Render a todo card with interactive elements."""
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

def mk_todo_form(project_id: int, todo=None, btn_text="Add Todo"):
    """Create todo creation/editing form."""
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
    """Create todo list for a project."""
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
                .global-info { background: #d1ecf1; padding: 10px; border-radius: 5px; margin-bottom: 20px; }
            """)
        ),
        air.Body(
            air.A("← Back to Projects", href="/", class_="back-link"),
            air.H1(f"📝 {project['name']} - Todos"),
            air.Div(
                air.P("🌐 Todo routes handled by todo_routes.py using global app"),
                class_="global-info"
            ),
            mk_todo_form(project_id),
            mk_todo_list(project_id)
        )
    )

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
