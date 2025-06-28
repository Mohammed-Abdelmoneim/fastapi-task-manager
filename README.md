<div align='center'>

<img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" width="20%" alt="FastAPI Logo"/>

# Task Management API
<em>A FastAPI-based Task Management API using Pydantic and SQLModel.</em>

<img src="https://img.shields.io/github/last-commit/Mohammed-Abdelmoneim/fastapi-task-manager?style=default&logo=git&logoColor=white&color=0080ff" alt="last-commit">
<img src="https://img.shields.io/github/languages/top/Mohammed-Abdelmoneim/fastapi-task-manager?style=default&color=0080ff" alt="repo-top-language">

</div>

---

## Features

- **CRUD Operations:** Create, Read, Update, Delete tasks
- **Filtering:** Filter tasks by status and priority
- **Pagination:** Support for `skip` and `limit` query parameters
- **Search:** Text search in title/description
- **Data Validation:** Comprehensive input validation using Pydantic
- **Error Handling:** Proper HTTP status codes and meaningful error messages
- **Database:** SQLite with SQLModel/SQLAlchemy integration
- **API Documentation:** Automatic OpenAPI/Swagger docs at `/docs`
- **Health Check:** `/health` endpoint for API and DB status

---
### Assumptions & Design Decisions
- The API uses SQLite for simplicity; the database file is created one directory above the app folder.

- All validation is handled via Pydantic models and custom validators.

- Both query parameter filtering and dedicated endpoints for status/priority are provided for flexibility.

- The API is designed to be RESTful and returns appropriate HTTP status codes for all operations.

### Requirements
See <code>requirements.txt</code> for the full list of dependencies.

## Setup Instructions

```bash
# Installation
pip install -r requirements.txt

# Run the application
python main.py

# Access API documentation
http://localhost:8000/docs
```

## Run Test
Note: Make sure your FastAPI App is running before executing the <code>tests.py</code>.

```bash
python tests/tests.py
```
## Example API calls

```bash
# Create a new task
curl -X POST "http://localhost:8000/tasks" \
     -H "Content-Type: application/json" \
     -d '{"title": "Sample Task", "priority": "high"}'

# List all tasks (with pagination)
curl "http://localhost:8000/tasks?skip=0&limit=5"

# Get a specific task
curl "http://localhost:8000/tasks/1"

# Update a task
curl -X PUT "http://localhost:8000/tasks/1" \
     -H "Content-Type: application/json" \
     -d '{"status": "completed"}'

# Delete a task
curl -X DELETE "http://localhost:8000/tasks/1"

# Filter by status
curl "http://localhost:8000/tasks/status/pending"

# Filter by priority
curl "http://localhost:8000/tasks/priority/high"

```

[![][back-to-top]](#top)

[back-to-top]: https://img.shields.io/badge/-BACK_TO_TOP-151515?style=flat-square
