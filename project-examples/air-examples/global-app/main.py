"""
Global App Air application example.
A todo/project management app using a global app instance shared across modules.

Run with: python main.py
Then visit: http://localhost:8003
"""

from globals import app, init_db, get_projects, create_project
from datetime import date

# Import modules to register their routes with the global app
import project_routes
import todo_routes

if __name__ == "__main__":
    # Initialize database
    init_db()
    
    # Add some sample data if database is empty
    if not get_projects():
        create_project("Sample Project")
        from globals import create_todo
        project_id = 1  # First project will have ID 1
        create_todo("Learn Global App pattern", date.today().isoformat(), project_id)
        create_todo("Build with shared app instance", date.today().isoformat(), project_id)
    
    print("🚀 Starting Air Global App example...")
    print("📂 Database: todos.db")
    print("🌐 Visit: http://localhost:8003")
    print("🌐 This example uses a global app instance shared across modules")
    
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
