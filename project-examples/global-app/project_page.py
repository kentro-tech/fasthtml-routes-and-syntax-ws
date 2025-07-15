from fasthtml.common import *
from datetime import date,datetime
from monsterui.all import *
from globals import app, db, Project

def ProjectCard(project:Project):
    if isinstance(project.created, str):
        created_date = datetime.fromisoformat(project.created.replace('Z', '+00:00')).strftime('%Y-%m-%d')
    else:
        created_date = project.created.strftime('%Y-%m-%d')
    
    return Card(
        A(Strong(project.name), href=f'/project/{project.id}'),
        P(f"Created: {created_date}", cls=TextPresets.muted_sm),
        id=f'project-{project.id}'
    )

def mk_project_list():
    return Grid(*(map(ProjectCard, db.projects())), cols=1)

def mk_project_form():
    return Form(
        DivLAligned(
            Input(id='project-name', name='name', placeholder='New Project Name'),
            Button('Create Project', cls=ButtonT.primary, hx_post=create_project, hx_target='#project-list', hx_swap='innerHTML')
        ),
        id='project-input', cls='mb-6'
    )

@app.post
async def create_project(name: str):
    if name.strip():
        db.projects.insert(Project(name=name.strip(), created=datetime.now()))
    return mk_project_list()

@app.get
async def index():
    "Main page showing all projects"
    return Titled('Projects', mk_project_form(), Div(mk_project_list(), id='project-list'))
