from fasthtml.common import *
from monsterui.all import *

app, rt = fast_app(hdrs=Theme.slate.headers())

from project_page import ar as project_ar
from todo_page import ar as todo_ar

project_ar.to_app(app)
todo_ar.to_app(app)

serve(port=5002)
