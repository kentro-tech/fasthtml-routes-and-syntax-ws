# Air Project Structure Examples

This directory contains four different project structure examples for Air applications, showing how to organize your code as your project grows from simple prototypes to complex applications.

## 📁 Examples Overview

| Pattern | Port | Best For | Complexity |
|---------|------|----------|------------|
| [single-file](single-file/) | 8000 | Prototypes, learning, simple tools | ⭐ |
| [python-modules](python-modules/) | 8001 | Small-medium apps, reusable components | ⭐⭐ |
| [api-router](api-router/) | 8002 | Large apps, team development | ⭐⭐⭐ |
| [global-app](global-app/) | 8003 | Plugin systems, shared resources | ⭐⭐ |

## 🚀 Quick Start

Each example is a complete, runnable todo/project management application with the same functionality but different organizational approaches.

### Prerequisites

```bash
# Install Air
pip install air

# Or using uv
uv add air
```

### Running the Examples

You can run all examples simultaneously (they use different ports):

```bash
# Single-file example (port 8000)
cd single-file
python main.py

# Python modules example (port 8001)
cd ../python-modules
python main.py

# API router example (port 8002)
cd ../api-router
python main.py

# Global app example (port 8003)
cd ../global-app
python main.py
```

Then visit:
- http://localhost:8000 - Single-file example
- http://localhost:8001 - Python modules example  
- http://localhost:8002 - API router example
- http://localhost:8003 - Global app example

## 🔍 Structure Comparison

### 1. Single-File Structure
```
single-file/
├── main.py          # Everything in one file
└── todos.db         # SQLite database
```

**When to use:** Prototypes, learning, simple scripts, MVPs

### 2. Python Modules Structure
```
python-modules/
├── main.py          # App setup and routes
├── db.py            # Database operations
├── pages.py         # Page layouts
├── components/      # Reusable UI components
│   ├── cards.py
│   └── forms.py
└── todos.db
```

**When to use:** Small-medium apps, when you need reusable components

### 3. API Router Structure
```
api-router/
├── main.py          # App setup and router inclusion
├── db.py            # Shared database operations
├── project_router.py # Project-related routes
├── todo_router.py   # Todo-related routes
└── todos.db
```

**When to use:** Large apps, team development, microservice-style organization

### 4. Global App Structure
```
global-app/
├── main.py          # Entry point with imports
├── globals.py       # Global app and shared resources
├── project_routes.py # Project routes using global app
├── todo_routes.py   # Todo routes using global app
└── todos.db
```

**When to use:** Plugin systems, shared resources, dynamic route registration

## ✨ Features Demonstrated

All examples show the same functionality with different organizational approaches:

- **Project Management**: Create and list projects
- **Todo Management**: Add, edit, delete, and complete todos
- **Interactive UI**: HTMX-powered dynamic updates
- **Date Handling**: Due dates with overdue highlighting
- **Data Persistence**: SQLite database with automatic setup
- **Air Tags**: HTML generation using Python classes
- **Form Handling**: Create and edit forms with validation
- **Routing**: GET/POST/DELETE routes with path parameters

## 🎯 Choosing the Right Structure

| Project Size | Team Size | Recommended Structure |
|--------------|-----------|----------------------|
| Prototype/Script | 1 developer | Single-file |
| Small App | 1-2 developers | Python modules |
| Medium App | 2-5 developers | API router |
| Large App | 5+ developers | API router |
| Plugin System | Any | Global app |

## 📚 Learning Path

1. **Start with single-file** to understand Air basics
2. **Move to python-modules** to learn component organization
3. **Try api-router** to understand FastAPI routing patterns
4. **Explore global-app** for plugin-style architectures

## 🔗 Related Documentation

- [Air Project Structure Guide](../docs/project-structure-guide.md) - Detailed documentation
- [Air Documentation](https://feldroy.github.io/air/) - Official Air docs
- [FastAPI Documentation](https://fastapi.tiangolo.com/) - Air is built on FastAPI

## 🛠️ Development Tips

- **Database**: Each example creates its own `todos.db` file with sample data
- **Hot Reload**: Use `uvicorn main:app --reload` for development
- **Dependencies**: All examples use only Air and standard library (except SQLite)
- **Ports**: Each example uses a different port so you can run them simultaneously
- **Styling**: Minimal inline CSS for simplicity - easily replaceable with your preferred CSS framework

## 🤝 Contributing

These examples are meant to be educational and practical starting points. If you find ways to improve them or have suggestions for additional patterns, please contribute!

Happy coding with Air! 🌬️
