# FastAPI Practice

A simple FastAPI practice project demonstrating API routes, Pydantic request validation, and a PostgreSQL database connection using `psycopg2`.

## Features

- FastAPI application instance with basic routes.
- PostgreSQL connection retry loop.
- Root endpoint that reads course records from a `courses` table.
- Path/query parameter example endpoint.
- Pydantic model for course creation payloads.

## Tech Stack

- Python
- FastAPI
- Pydantic
- PostgreSQL
- psycopg2

## Project Structure

```text
.
|-- main.py          # Main FastAPI application
`-- app/main.py      # Additional app module copy/experiment
```

## Getting Started

Install dependencies:

```bash
pip install fastapi uvicorn psycopg2-binary
```

Create a PostgreSQL database named `practice` with a `courses` table, then update the connection values in `main.py` if needed.

Run the API:

```bash
uvicorn main:app --reload
```

Open the interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

## Notes

Database credentials are currently hard-coded for local practice. Move them to environment variables before using this pattern in a shared or production project.
