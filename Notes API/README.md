# Notes REST API

A clean, production-ready RESTful API for managing notes built with **FastAPI**, **SQLAlchemy ORM**, **Pydantic v2**, and **MySQL** (with SQLite fallback).

---

## Features

- **Framework**: FastAPI for fast, modern web API development.
- **Database Support**: Native **MySQL** integration via `PyMySQL` driver with SQLAlchemy connection pooling, plus SQLite fallback.
- **Validation**: Pydantic v2 schemas for request payload and response validation.
- **CRUD Operations**: Full RESTful operations (Create, Read All, Read One, Update, Delete).
- **Session Management**: Clean dependency injection with request-scoped database sessions (`get_db`).
- **Interactive API Docs**: Automatic Swagger UI (`/docs`) and ReDoc (`/redoc`).
- **Testing**: Automated unit and integration test suite using `pytest` and `TestClient`.

---

## Directory Structure

```
Notes API/
├── app/
│   ├── __init__.py
│   ├── database.py       # Engine config (MySQL & SQLite), SessionLocal, get_db dependency
│   ├── models.py         # SQLAlchemy Note ORM Model
│   ├── schemas.py        # Pydantic v2 request/response schemas
│   ├── crud.py           # Database CRUD utility functions
│   ├── main.py           # FastAPI app entry point & lifespan setup
│   └── routers/
│       ├── __init__.py
│       └── notes.py      # Note REST API router and endpoints
├── tests/
│   ├── __init__.py
│   └── test_notes.py     # pytest automated test suite
├── .env.example          # Environment variable template
├── .gitignore            # Git ignore rules
├── requirements.txt      # Project dependencies (FastAPI, PyMySQL, SQLAlchemy, etc.)
└── README.md             # Project documentation
```

---

## Installation & Setup

1. **Clone or navigate to the project directory**:
   ```bash
   cd "c:/Users/princ/Prince Lakhani/APIs/Notes API"
   ```

2. **Create and activate a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   # On Windows (PowerShell):
   .\venv\Scripts\Activate.ps1
   # On Linux/macOS:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## Database Configuration (MySQL)

Create a MySQL database (e.g., `notes_db`) in your MySQL server:

```sql
CREATE DATABASE notes_db;
```

Set the `DATABASE_URL` environment variable before running the application:

### Connection String Format
```text
mysql+pymysql://<username>:<password>@<host>:<port>/<database_name>
```

### Setting `DATABASE_URL` on Windows (PowerShell)
```powershell
$env:DATABASE_URL="mysql+pymysql://root:password@localhost:3306/notes_db"
```

### Setting `DATABASE_URL` on Linux / macOS / CMD
```bash
export DATABASE_URL="mysql+pymysql://root:password@localhost:3306/notes_db"
```

> **Note**: If `DATABASE_URL` is not set, the application will default to a local SQLite database (`sqlite:///./notes.db`) for seamless development.

---

## Running the API Server

Start the application server using `uvicorn`:

```bash
uvicorn app.main:app --reload
```

The server will start at `http://127.0.0.1:8000`.

- **Root Endpoint**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Swagger Documentation**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc Documentation**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## API Endpoints Summary

| Method | Endpoint | Status Code | Description |
| :--- | :--- | :--- | :--- |
| `POST` | `/notes/` | `201 Created` | Create a new note |
| `GET` | `/notes/` | `200 OK` | Get all notes (supports `skip` & `limit` query parameters) |
| `GET` | `/notes/{id}` | `200 OK` / `404 Not Found` | Get a specific note by ID |
| `PUT` | `/notes/{id}` | `200 OK` / `404 Not Found` | Update a note by ID |
| `DELETE` | `/notes/{id}` | `204 No Content` / `404 Not Found` | Delete a note by ID |

---

## Data Schema

### Note Object
Each Note consists of:

- `id` (integer): Auto-generated primary key.
- `title` (string): Title of the note (1 to 255 characters).
- `content` (string): Body text of the note.
- `created_at` (datetime, UTC): Auto-generated creation timestamp.
- `updated_at` (datetime, UTC): Auto-updated modification timestamp.

---

## Running Automated Tests

Run the test suite using `pytest`:

```bash
pytest -v
```

The tests use an isolated in-memory database to execute quickly and independently of your production MySQL server.
