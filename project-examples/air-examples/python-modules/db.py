"""
Database module for the Air python-modules example.
Handles all database operations for projects and todos.
"""

import sqlite3
from datetime import datetime
from typing import List, Dict, Optional

DB_FILE = "todos.db"

def init_db():
    """Initialize the database with required tables."""
    conn = sqlite3.connect(DB_FILE)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            created TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done INTEGER DEFAULT 0,
            due TEXT NOT NULL,
            project_id INTEGER NOT NULL,
            FOREIGN KEY (project_id) REFERENCES projects (id)
        )
    """)
    conn.commit()
    conn.close()

def get_projects() -> List[Dict]:
    """Get all projects."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.execute("SELECT id, name, created FROM projects ORDER BY created DESC")
    projects = [{"id": row[0], "name": row[1], "created": row[2]} for row in cursor.fetchall()]
    conn.close()
    return projects

def get_project(project_id: int) -> Optional[Dict]:
    """Get a single project by ID."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.execute("SELECT id, name, created FROM projects WHERE id = ?", (project_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"id": row[0], "name": row[1], "created": row[2]}
    return None

def create_project(name: str) -> int:
    """Create a new project and return its ID."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.execute("INSERT INTO projects (name, created) VALUES (?, ?)", 
                         (name, datetime.now().isoformat()))
    project_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return project_id

def get_todos(project_id: int) -> List[Dict]:
    """Get todos for a project."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.execute("""
        SELECT id, title, done, due, project_id 
        FROM todos 
        WHERE project_id = ? 
        ORDER BY due, id
    """, (project_id,))
    todos = [{"id": row[0], "title": row[1], "done": bool(row[2]), 
              "due": row[3], "project_id": row[4]} for row in cursor.fetchall()]
    conn.close()
    return todos

def get_todo(todo_id: int) -> Optional[Dict]:
    """Get a single todo by ID."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.execute("SELECT id, title, done, due, project_id FROM todos WHERE id = ?", (todo_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"id": row[0], "title": row[1], "done": bool(row[2]), 
                "due": row[3], "project_id": row[4]}
    return None

def create_todo(title: str, due: str, project_id: int) -> int:
    """Create a new todo and return its ID."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.execute("""
        INSERT INTO todos (title, done, due, project_id) 
        VALUES (?, 0, ?, ?)
    """, (title, due, project_id))
    todo_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return todo_id

def update_todo(todo_id: int, title: str = None, done: bool = None, due: str = None):
    """Update a todo."""
    conn = sqlite3.connect(DB_FILE)
    if title is not None:
        conn.execute("UPDATE todos SET title = ? WHERE id = ?", (title, todo_id))
    if done is not None:
        conn.execute("UPDATE todos SET done = ? WHERE id = ?", (int(done), todo_id))
    if due is not None:
        conn.execute("UPDATE todos SET due = ? WHERE id = ?", (due, todo_id))
    conn.commit()
    conn.close()

def delete_todo(todo_id: int):
    """Delete a todo."""
    conn = sqlite3.connect(DB_FILE)
    conn.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
    conn.commit()
    conn.close()
