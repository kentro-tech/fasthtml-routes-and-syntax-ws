from fasthtml.common import *
from monsterui.all import *
from components.forms import mk_todo_form, mk_project_form
from components.cards import ProjectCard, TodoCard

def mk_project_list(projects_list):
    return Grid(*[ProjectCard(p.name, p.created, p.id) for p in projects_list], cols=1)

def ProjectPage(projects_list):
    return Titled('Projects', mk_project_form(), Div(mk_project_list(projects_list), id='project-list'))


def mk_todo_list(project_id, todos_list):  
    return Grid(*[TodoCard(t.due, t.done, t.title, t.id) for t in todos_list], cols=1)


def ProjectTodosPage(name, project_id, todos_list):
    return Titled(
        f'{name} - Todos',
        A('← Back to Projects', href='/', cls='mb-4 inline-block'),
        mk_todo_form(project_id),
        Div(mk_todo_list(project_id, todos_list), id='todo-list')
    )
