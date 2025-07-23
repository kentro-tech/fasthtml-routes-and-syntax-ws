from fasthtml.common import *
from monsterui.all import *
from datetime import date

def mk_project_form():
    return Form(
        DivLAligned(
            Input(id='project-name', name='name', placeholder='New Project Name'),
            Button('Create Project', cls=ButtonT.primary, hx_post="/create_project", hx_target='#project-list', hx_swap='innerHTML')
        ),
        id='project-input', cls='mb-6')


def mk_todo_form(project_id, todo=None, btn_text="Add"):
    """Create a form for todo creation/editing with optional pre-filled values"""
    if todo is None:
        title=''
        done=False
        due=date.today()
        id=None
    else:
        title = todo.title
        done = todo.done
        due = todo.due
        id = todo.id
    
    inputs = [Input(id='new-title', name='title',value=title, placeholder='New Todo'),
              Input(id='new-done',  name='done', value=done,  hidden=True),
              Input(id='new-due',   name='due',  value=due),
              Input(id='new-project-id', name='project_id', value=project_id, hidden=True)]
    
    if id: inputs.append(Input(id='new-id', name='id', value=id, hidden=True))
        
    return Form(DivLAligned(
        *inputs,
        Button(btn_text, cls=ButtonT.primary, hx_post="/upsert_todo", hx_target='#todo-list', hx_swap='innerHTML')),
        id='todo-input', cls='mb-6')