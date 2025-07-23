# API Router Air Example

A todo/project management application using FastAPI's APIRouter for modular routing. This pattern is excellent for larger applications where you want to organize routes by feature or domain.

## Features

- Same functionality as previous examples
- Organized using FastAPI's APIRouter pattern:
  - `project_router.py` - All project-related routes
  - `todo_router.py` - All todo-related routes
  - `main.py` - Application setup and router inclusion
  - `db.py` - Shared database operations

## File Structure

```
api-router/
├── main.py              # Application setup and router inclusion
├── db.py                # Shared database operations
├── project_router.py    # Project-related routes and components
├── todo_router.py       # Todo-related routes and components
├── README.md            # This file
└── todos.db             # SQLite database (created on first run)
```

## Running the Example

1. Make sure Air is installed:
   ```bash
   pip install air
   ```

2. Run the application:
   ```bash
   python main.py
   ```

3. Visit http://localhost:8002

## Key Benefits of API Router Structure

- **Feature Separation**: Each router handles a specific domain (projects vs todos)
- **Team Development**: Different developers can work on different routers
- **Scalability**: Easy to add new feature routers without touching existing code
- **Testing**: Individual routers can be tested in isolation
- **Microservice Ready**: Routers can be easily extracted into separate services
- **Clear Dependencies**: Each router has its own components and logic

## Router Organization

### `project_router.py`
- Project listing and creation
- Project-specific components (ProjectCard, forms)
- Main index page

### `todo_router.py`
- Todo CRUD operations
- Todo-specific components (TodoCard, forms)
- Project todos page

### `main.py`
- Minimal application setup
- Router registration
- Database initialization

## Air + FastAPI Router Features

- Uses FastAPI's `APIRouter` for modular routing
- Each router can have its own components and logic
- Routers are included in the main app with `app.include_router()`
- Maintains Air's simplicity while adding organizational structure
- Perfect for team development and larger applications

## When to Use This Pattern

- **Medium to Large Applications**: When single-file or simple modules aren't enough
- **Team Development**: Multiple developers working on different features
- **Domain Separation**: Clear boundaries between different business domains
- **Microservice Preparation**: When you might split features into separate services later
- **API + Web Hybrid**: When you want clear separation between web pages and API endpoints

This pattern scales well and is the recommended approach for production Air applications.
