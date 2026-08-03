# Flight Menu Management API

A RESTful API built with **FastAPI** for managing in-flight meal menus.

The application allows airlines to create, search, update and logically delete flight menus while supporting multilingual dish information (Spanish and English), pagination, filtering and clean layered architecture.

---

## Overview

Flight Menu Management API provides a centralized service for managing menus associated with commercial flights.

Each menu belongs to a flight and contains one or more dishes with multilingual descriptions. The API validates duplicate menus, supports logical deletion, and exposes OpenAPI documentation out of the box.

---

## Key Features

- Complete CRUD for flight menus.
- Flight-based menu association.
- Multilingual dishes (Spanish / English).
- Search menus using multiple filters.
- Pagination support.
- Soft delete.
- Duplicate menu validation.
- Automatic OpenAPI documentation.
- Layered Architecture.
- Repository Pattern.

---

## Tech Stack

| Category | Technology |
|----------|------------|
| Language | Python 3.13 |
| Framework | FastAPI |
| ORM | SQLAlchemy 2.0 |
| Database | PostgreSQL |
| Database Migrations | Alembic |
| Validation | Pydantic v2 |
| API Documentation | OpenAPI / Swagger UI |
| Dependency Management | pip |
| Containerization | Docker & Docker Compose |

---

## Architecture

The project follows a layered architecture that separates HTTP handling, business rules and persistence into independent layers.

### Design Principles

- Layered Architecture
- Repository Pattern
- Service Layer
- Dependency Injection
- Soft Delete Strategy
- RESTful API Design

```
                HTTP Request
                      │
                      ▼
                FastAPI Router
                      │
                      ▼
                 Service Layer
                      │
                      ▼
              Repository Layer
                      │
                      ▼
               SQLAlchemy ORM
                      │
                      ▼
                 PostgreSQL
```

---

## Project Structure

```text
flight-menu-management/
│
├── alembic/                  # Database migrations
│
├── app/
│   ├── auth/                 # Authentication
│   ├── core/                 # Shared business utilities
│   ├── database/             # Database configuration
│   ├── dependencies/         # Dependency Injection
│   ├── exceptions/           # Custom exceptions
│   ├── filters/              # Search filters
│   ├── models/               # SQLAlchemy models
│   ├── repositories/         # Data access layer
│   ├── routers/              # REST endpoints
│   ├── schemas/              # Pydantic DTOs
│   └── services/             # Business logic
│
├── docs/                     # Architecture Decision Records
├── tests/                    # Unit & integration tests
│
├── docker-compose.yml
├── requirements.txt
└── README.md
```

Each layer has a single responsibility:

- **Routers** expose HTTP endpoints.
- **Services** contain business rules.
- **Repositories** encapsulate persistence.
- **Models** represent database entities.
- **Schemas** define API contracts.
- **Dependencies** provide dependency injection.

---

## Installation

### Prerequisites

- Python 3.13+
- PostgreSQL 16+
- Git
- Docker & Docker Compose (optional)

---

### Clone the repository

```bash
git clone https://github.com/<your-username>/flight-menu-management.git

cd flight-menu-management
```

---

### Create a virtual environment

```bash
python -m venv .venv
```

Activate it.

macOS / Linux

```bash
source .venv/bin/activate
```

Windows

```powershell
.venv\Scripts\activate
```

---

### Install dependencies

```bash
pip install -r requirements.txt
```

---

### Configure environment variables

Create a `.env` file in the project root.

```env
DATABASE_URL=postgresql+psycopg://flight_menu_user:password@localhost:5432/flight_menu_db
```

---

### Run database migrations

```bash
alembic upgrade head
```

---

## Environment Variables

Example:

```env
DATABASE_URL=postgresql+psycopg://flight_menu_user:password@localhost:5432/flight_menu_db

# Planned feature
JWT_SECRET_KEY=change_this_secret_key
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60
```

| Variable | Required | Description |
|----------|:--------:|-------------|
| DATABASE_URL | ✅ | PostgreSQL connection string |
| JWT_SECRET_KEY | 🚧 | Secret key used to sign JWT tokens |
| JWT_ALGORITHM | 🚧 | JWT signing algorithm |
| JWT_ACCESS_TOKEN_EXPIRE_MINUTES | 🚧 | Access token expiration |

> **Note:** Currently only `DATABASE_URL` is required. JWT variables are documented in advance because authentication is planned for the next iteration.

---

## Running the Project

Start the API.

```bash
uvicorn app.main:app --reload
```

The application will be available at:

```
http://localhost:8000
```

---

## Running with Docker

```bash
docker compose up --build
```

---

## API Documentation

FastAPI automatically exposes interactive documentation.

| Documentation | URL |
|---------------|-----|
| Swagger UI | http://localhost:8000/docs |
| ReDoc | http://localhost:8000/redoc |

### Implemented Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | `/api/v1/flights` | List available flights |
| GET | `/api/v1/menus` | List menus |
| POST | `/api/v1/menus` | Create menu |
| POST | `/api/v1/menus/search` | Search menus |
| GET | `/api/v1/menus/{id}` | Retrieve menu |
| PUT | `/api/v1/menus/{id}` | Update menu |
| DELETE | `/api/v1/menus/{id}` | Soft delete menu |

---

## Useful Commands

Run migrations

```bash
alembic upgrade head
```

Create a migration

```bash
alembic revision --autogenerate -m "description"
```

Run the application

```bash
uvicorn app.main:app --reload
```

---

## Testing

Automated testing is currently under development.

The project will include:

- Unit tests
- Integration tests
- Pytest
- Coverage reports (>60%)

---

## Future Improvements

Planned enhancements include:

- JWT authentication and authorization.
- Structured logging.
- Bulk menu upload from CSV and Excel files.
- Automated testing with Pytest and coverage reports.
- CI/CD pipeline.
- Role-Based Access Control (RBAC).
- API versioning.
- Semantic dish search using configurable keyword dictionaries and synonym mapping to improve menu filtering (e.g. *beef*, *steak*, *sirloin*, *meat*).

---

## License
Samuel Cruz

This project is licensed under the MIT License.