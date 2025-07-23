"""
Project-related routes using FastAPI's APIRouter.
Handles all project management functionality.
"""

import air
from fastapi import APIRouter, Form
from datetime import datetime
from db import get_projects, get_project, create_project

router = APIRouter()

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

@router.post("/create_project")
async def create_project_route(name: str = Form(...)):
    """Create a new project."""
    if name.strip():
        create_project(name.strip())
    return mk_project_list()

@router.get("/")
async def index():
    """Main page showing all projects."""
    return air.Html(
        air.Head(
            air.Title("Todo Projects - API Router Example"),
            air.Script(src="https://unpkg.com/htmx.org@1.9.10"),
            air.Style("""
                body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
                h1 { color: #333; }
                .container { margin: 20px 0; }
                a { color: #007bff; text-decoration: none; }
                a:hover { text-decoration: underline; }
                .router-info { background: #e3f2fd; padding: 10px; border-radius: 5px; margin-bottom: 20px; }
            """)
        ),
        air.Body(
            air.H1("📋 Todo Projects"),
            air.Div(
                air.P("🔀 This example uses FastAPI's APIRouter for modular routing."),
                air.P("📁 Check out: project_router.py and todo_router.py"),
                class_="router-info"
            ),
            mk_project_form(),
            mk_project_list()
        )
    )
