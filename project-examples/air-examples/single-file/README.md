# Single-File Air Example

A complete todo/project management application built with Air in a single file.

## Features

- Create and manage projects
- Add todos to projects with due dates
- Mark todos as complete
- Edit and delete todos
- HTMX-powered interactivity
- SQLite database

## Running the Example

1. Make sure Air is installed:
   ```bash
   pip install air
   ```

2. Run the application:
   ```bash
   python main.py
   ```

3. Visit http://localhost:8000

## What You'll See

- A list of projects on the main page
- Click on a project to see its todos
- Add new projects and todos using the forms
- Interactive todo management with checkboxes, edit, and delete buttons

## Database

The app creates a `todos.db` SQLite file automatically with sample data on first run.

## Key Air Features Demonstrated

- Air Tags for HTML generation
- HTMX integration for dynamic updates
- Route definitions with `@app.get`, `@app.post`, etc.
- Form handling and data binding
- Component-based architecture within a single file

This example shows how quickly you can build a functional web application with Air!
