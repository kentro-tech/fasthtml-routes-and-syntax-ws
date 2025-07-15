from fasthtml.common import *
from datetime import date,datetime
from monsterui.all import *
from globals import app, db, Todo
def tid(id): return f'todo-{id}'


def TodoCard(todo:Todo):
    
    dd = datetime.strptime(todo.due, '%Y-%m-%d').date()
    due_date = Strong(dd.strftime('%Y-%m-%d'),style= "" if date.today() <= dd else "background-color: red;") 
    _targets = {'hx_target':f'#{tid(todo.id)}', 'hx_swap':'outerHTML'}
    done   = CheckboxX(       hx_get   =toggle_done.to(id=todo.id), **_targets, checked=todo.done), 
    delete = Button('delete', hx_delete=delete_todo.to(id=todo.id), **_targets)
    edit   = Button('edit',   hx_get   =edit_todo  .to(id=todo.id), **_targets)
    style = Del if todo.done else noop
    return Card(DivLAligned(done, 
                            style(Strong(todo.title, target_id='current-todo')), 
                            style(P(due_date,cls=TextPresets.muted_sm)),
                            edit,
                            delete),
                id=tid(todo.id))

def mk_todo_list(project_id):  return Grid(*(map(TodoCard,db.todos(where=f'project_id={project_id}', order_by='due'))), cols=1)

@app.delete
async def delete_todo(id:int):
    "Delete if it exists, if not someone else already deleted it so no action needed"
    try: db.todos.delete(id)
    except NotFoundError: pass


@app.get('/project/{project_id}')
async def project_todos(project_id: int):
    "Todo list for a specific project"
    project = db.projects[project_id]
    return Titled(
        f'{project.name} - Todos',
        A('← Back to Projects', href='/', cls='mb-4 inline-block'),
        mk_todo_form(project_id),
        Div(mk_todo_list(project_id), id='todo-list')
    )

@app.post 
async def upsert_todo(todo:Todo):
    if todo.title.strip(): db.todos.insert(todo,replace=True)
    return mk_todo_list(todo.project_id),mk_todo_form(todo.project_id)(hx_swap_oob='true',hx_target='#todo-input',hx_swap='outerHTML')

@app.get 
async def toggle_done(id:int):
    "Reverses done boolean in the database and returns the todo (rendered with __ft__)"
    return TodoCard(db.todos.update(Todo(id=id, done=not db.todos[id].done)))

def mk_todo_form(project_id, todo=None, btn_text="Add"):
    """Create a form for todo creation/editing with optional pre-filled values"""
    if todo is None:
        todo = Todo(title='', done=False, due=date.today(), id=None, project_id=project_id)
    
    inputs = [Input(id='new-title', name='title',value=todo.title, placeholder='New Todo'),
              Input(id='new-done',  name='done', value=todo.done,  hidden=True),
              Input(id='new-due',   name='due',  value=todo.due),
              Input(id='new-project-id', name='project_id', value=project_id, hidden=True)]
    
    if todo.id: inputs.append(Input(id='new-id', name='id', value=todo.id, hidden=True))
        
    return Form(DivLAligned(
        *inputs,
        Button(btn_text, cls=ButtonT.primary, post=upsert_todo,hx_target='#todo-list', hx_swap='innerHTML')),
        id='todo-input', cls='mb-6')

@app.get 
async def edit_todo(id:int): 
    todo = db.todos[id]
    return Card(mk_todo_form(todo.project_id, todo, btn_text="Save"))