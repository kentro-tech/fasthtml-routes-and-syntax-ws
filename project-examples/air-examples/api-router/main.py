"""
API Router Air application example.
A todo/project management app using FastAPI's APIRouter for modular routing.

Run with: python main.py
Then visit: http://localhost:8002
"""

import air
from db import init_db, get_projects, create_project
from datetime import date

app = air.Air()

# Import and include routers
from project_router import router as project_router
from todo_router import router as todo_router

app.include_router(project_router)
app.include_router(todo_router)

if __name__ == "__main__":
    # Initialize database
    init_db()
    
    # Add some sample data if database is empty
    if not get_projects():
        create_project("Sample Project")
        from db import create_todo
        project_id = 1  # First project will have ID 1
        create_todo("Learn API Router pattern", date.today().isoformat(), project_id)
        create_todo("Build scalable app structure", date.today().isoformat(), project_id)
    
    print("🚀 Starting Air API Router example...")
    print("📂 Database: todos.db")
    print("🌐 Visit: http://localhost:8002")
    print("📚 This example uses FastAPI's APIRouter for modular routing")
    
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
