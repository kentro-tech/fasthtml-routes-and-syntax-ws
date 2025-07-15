import marimo

__generated_with = "0.14.10"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    from fasthtml.common import Ul, Li, P, Div, Script, H1, H2, Strong, Span, Label, Input, Form, Br
    return Br, Div, Form, Input, Label, Li, P, Script, Span, Strong, Ul, mo


@app.cell
def _(Div, Script, mo):
    def show(*c):
        return mo.Html(str(Div(Script(src="https://cdn.tailwindcss.com"),*c)))
    return (show,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""# FastHTML Fasttag Patterns""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Conditionals""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### If Statement""")
    return


@app.cell
def _(P, show):
    # Traditional if/else
    is_logged_in = True

    if is_logged_in:
        greeting = P("Welcome back!")
    else:
        greeting = P("Please log in")

    show(greeting)
    return (is_logged_in,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### Inline If Statement""")
    return


@app.cell
def _(P, is_logged_in, show):
    # Inline conditional
    status = P("Welcome back!" if is_logged_in else "Please log in")

    show(status)
    return


@app.cell
def _(Span, show):
    # Conditional styling
    score = 50

    grade_display = Span(
        f"Score: {score}",
        style=f"color: {'green' if score >= 70 else 'red'};"
    )

    show(grade_display)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### Conditional Element Inclusion""")
    return


@app.cell
def _(Br, Form, Input, Label, show):
    # Building form with conditional fields
    show_email = True

    form_fields = [
        Label("Name:"),
        Input(name="name", placeholder="Enter name", cls='border'),
        Br()
    ]

    if show_email:
        form_fields.extend([
            Label("Email:"),
            Input(name="email", type="email", placeholder="Enter email", cls='border')
        ])

    form = Form(*form_fields)

    show(form)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### Pattern Matching""")
    return


@app.cell
def _(Div, Span, show):
    # Match pattern (Python 3.10+)
    def status_badge(status):
        match status:
            case "active":
                return Span("Active", style="color: green;")
            case "pending":
                return Span("Pending", style="color: orange;")
            case "inactive":
                return Span("Inactive", style="color: red;")
            case _:
                return Span("Unknown", style="color: gray;")

    # Example usage
    statuses = ["active", "pending", "inactive", "other"]
    badges = Div(*[status_badge(s) for s in statuses], cls='space-x-10')

    show(badges)
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""## List Iteration Patterns""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""### For Loops""")
    return


@app.cell
def _(mo):
    todos = mo.ui.array([
        mo.ui.text("Cleaning"),
        mo.ui.text("Shopping"),
        mo.ui.text("Call Mom"),
        mo.ui.text()],
        label='todos')
    todos
    return (todos,)


@app.cell
def _(Li, P, Ul, show, todos):
    # Build list of elements
    li_elements = []
    for todo in todos.value:
        if todo:
            li_elements.append(Li(todo))

    # Create unordered list
    ul_with_for = Ul(*li_elements, cls='list-disc')

    show(
        P("My Todos!", cls='text-2xl text-bold mb-2'),
        ul_with_for)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""### List Comprehension""")
    return


@app.cell
def _(Li, P, Ul, show, todos):
    _list_items = [Li(todo) for todo in todos.value if todo]
    ul_with_comprehension = Ul(*_list_items, cls='list-disc')

    show(
        P("My Todos!", cls='text-2xl text-bold mb-2'),
        ul_with_comprehension)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""### Map Function""")
    return


@app.cell
def _(Div, P, Strong, show):
    # Data for cards
    people = [
        {'name': 'Alice', 'age': 30},
        {'name': 'Bob', 'age': 25},
        {'name': 'Charlie', 'age': 35}
    ]

    def PersonCard(person):
        return Div(
            Strong(person['name']),
            P(f"Age: {person['age']}"),
            cls='border border-solid max-w-28'
        )

    cards_with_map = Div(*map(PersonCard, people), cls='space-y-3')
    show(cards_with_map)
    return


if __name__ == "__main__":
    app.run()
