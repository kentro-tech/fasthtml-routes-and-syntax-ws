# Global App Air Example

A todo/project management application using a global app instance shared across modules. This pattern is great for plugin architectures and when you need dynamic route registration.

## Features

- Same functionality as previous examples
- Uses a global app instance pattern:
  - `globals.py` - Global app instance and shared resources
  - `project_routes.py` - Project routes registered on global app
  - `todo_routes.py` - Todo routes registered on global app
  - `main.py` - Entry point that imports modules to register routes

## File Structure

```
global-app/
├── main.py              # Entry point and module imports
├── globals.py           # Global app instance and database operations
├── project_routes.py    # Project routes using global app
├── todo_routes.py       # Todo routes using global app
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

3. Visit http://localhost:8003

## Key Benefits of Global App Structure

- **Simple Registration**: Routes are registered by importing modules
- **Shared Resources**: Easy to share app instance, database, and other resources
- **Plugin Architecture**: New features can be added by creating new modules
- **Minimal Boilerplate**: Very little setup code in main.py
- **Dynamic Loading**: Modules can be imported conditionally

## How It Works

### 1. Global App Instance (`globals.py`)
```python
import air
app = air.Air()  # Global app instance

# Shared database operations
def get_projects(): ...
def create_project(): ...
```

### 2. Route Modules Import Global App
```python
# project_routes.py
from globals import app

@app.get("/")  # Routes registered on global app
async def index():
    return ...
```

### 3. Main Entry Point Imports Modules
```python
# main.py
from globals import app

# Import modules to register their routes
import project_routes  # Registers project routes
import todo_routes     # Registers todo routes

# App is now ready with all routes
```

## Air + Global App Features

- Single app instance shared across modules
- Routes registered by importing modules
- Easy resource sharing (database, config, etc.)
- Very simple main.py entry point
- Great for plugin-style architectures

## When to Use This Pattern

- **Plugin Systems**: When you want modules to self-register functionality
- **Microframework Style**: When you want minimal boilerplate
- **Shared Resources**: When many modules need access to the same resources
- **Simple Deployment**: When you want all routes in one app instance
- **Dynamic Loading**: When you might conditionally load modules

## Considerations

- **Import Order**: Make sure globals.py is imported before route modules
- **Testing**: Global state can make testing more complex
- **Circular Imports**: Be careful about module dependencies

This pattern is particularly useful for applications that need to be extensible through plugins or when you want to keep the main application setup very simple.
