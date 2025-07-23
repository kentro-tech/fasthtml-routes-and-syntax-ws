"""
Form components for creating and editing projects and todos.
Reusable form UI components for the Air python-modules example.
"""

import air
from datetime import date

def mk_project_form():
    """Create project creation form."""
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
