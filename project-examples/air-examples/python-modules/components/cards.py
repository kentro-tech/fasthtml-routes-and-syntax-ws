"""
Card components for displaying projects and todos.
Reusable UI components for the Air python-modules example.
"""

import air
from datetime import date, datetime

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

def ProjectCard(project):
    """Render a project card."""
    created_date = datetime.fromisoformat(project["created"]).strftime('%Y-%m-%d')
    return air.Div(
        air.H3(
            air.A(
                project["name"], 
                href=f'/project/{project["id"]}', 
                style="text-decoration: none; color: #007bff;"
            )
        ),
        air.P(f"Created: {created_date}", style="color: #666; margin: 5px 0;"),
        id=f'project-{project["id"]}',
        style="border: 1px solid #ddd; padding: 15px; margin-bottom: 15px; border-radius: 5px; background: #f8f9fa;"
    )
