from fasthtml.common import *

app,rt = fast_app()

@rt
def index():
    return Main(
        Button('Click me',
            hx_get='/click',
            hx_target='#content',
        ),
        Div(id='content')
    )

@rt
def click():
    return P('Clicked'), P('Another Clicked')

serve(port=5005)