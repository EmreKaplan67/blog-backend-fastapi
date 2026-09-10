# Blog Backend

A simple FastAPI blog backend for creating, reading, updating, and deleting blog posts. It uses SQLAlchemy with PostgreSQL, JWT-based admin authentication via Supabase, and Alembic for database migrations.

## Features

- List blog posts with pagination
- Fetch a single post by slug
- Create a new post
- Update an existing post
- Delete a post
- Admin-only write operations protected by JWT validation
- Automatic slug generation for post titles

## Tech Stack

- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- Supabase Auth
- Python 3.14+
- Uvicorn

## Project Structure

```text
blog/
├── src/
│   └── blog/
│       ├── app.py
│       ├── auth.py
│       ├── db.py
│       ├── models.py
│       ├── schemas.py
│       ├── utils.py
│       └── alembic/
├── pyproject.toml
├── README.md
```

## Prerequisites

- Python 3.14 or newer
- PostgreSQL database
- Supabase project with authentication enabled


## API Endpoints

### Public

- `GET /posts` - Get all posts with pagination
- `GET /posts/{slug}` - Get a single post by slug

### Admin only

- `POST /posts` - Create a new post
- `PATCH /posts/{post_id}` - Update a post
- `DELETE /posts/{post_id}` - Delete a post

All admin actions require a valid bearer token from Supabase.


