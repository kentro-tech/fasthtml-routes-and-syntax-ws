# Python Modules Air Example

A todo/project management application organized into logical Python modules for better code organization and reusability.

## Features

- Same functionality as single-file example
- Organized into logical modules:
  - `db.py` - Database operations
  - `components/` - Reusable UI components
  - `pages.py` - Page layouts and templates
  - `main.py` - Application setup and routes

## File Structure

```
python-modules/
├── main.py              # Application setup and routes
├── db.py                # Database models and operations
├── pages.py             # Page layouts and templates
├── components/
│   ├── __init__.py      # Package initialization
│   ├── cards.py         # Card components (TodoCard, ProjectCard)
│   └── forms.py         # Form components
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

3. Visit http://localhost:8001

## Key Benefits of This Structure

- **Separation of Concerns**: Database logic, UI components, and routing are separated
- **Reusability**: Components can be easily reused across different pages
- **Maintainability**: Easier to find and modify specific functionality
- **Testing**: Individual modules can be unit tested
- **Team Development**: Different developers can work on different modules

## Air Features Demonstrated

- Modular component architecture
- Clean separation between data, presentation, and routing
- Reusable form and card components
- Page templates that compose components
- Import-based code organization while maintaining Air's simplicity

This structure works well for small to medium-sized applications where you need better organization than a single file but don't need the complexity of API routers.
