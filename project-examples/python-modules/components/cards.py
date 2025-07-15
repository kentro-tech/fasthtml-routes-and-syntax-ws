from fasthtml.common import *
from monsterui.all import *
from datetime import date,datetime

def tid(id): return f'todo-{id}'

def TodoCard(due, done, title, id):
    dd = datetime.strptime(due, '%Y-%m-%d').date()
    due_date = Strong(dd.strftime('%Y-%m-%d'),style= "" if date.today() <= dd else "background-color: red;") 
    _targets = {'hx_target':f'#{tid(id)}', 'hx_swap':'outerHTML'}
    checkbox = CheckboxX(hx_get=f"/toggle_done?id={id}", **_targets, checked=done)
    delete = Button('delete', hx_delete=f"/delete_todo?id={id}", **_targets)
    edit   = Button('edit',   hx_get   =f"/edit_todo?id={id}", **_targets)
    style = Del if done else noop
    return Card(DivLAligned(checkbox, 
                            style(Strong(title, target_id='current-todo')), 
                            style(P(due_date,cls=TextPresets.muted_sm)),
                            edit,
                            delete),
                id=tid(id))


def ProjectCard(name, created, id):
    if isinstance(created, str):
        created_date = datetime.fromisoformat(created.replace('Z', '+00:00')).strftime('%Y-%m-%d')
    else:
        created_date = created.strftime('%Y-%m-%d')
    
    return Card(
        A(Strong(name), href=f'/project/{id}'),
        P(f"Created: {created_date}", cls=TextPresets.muted_sm),
        id=f'project-{id}'
    )