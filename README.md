# POS (Point of Sale) API

A REST API for a small-to-medium retail business built with **FastAPI, SQLAlchemy, and PostgreSQL**. It manages inventory, customers, staff accounts, and sales.

## Features

* **Inventory Management** — categories, suppliers, products, stock, and pricing
* **Sales Processing** — sales, sale items, and multiple payment methods
* **Customer Management** — customer records linked to purchase history
* **User Access Control** — staff accounts with Admin and Cashier roles
* **Receipts** — unique receipt generated for each sale
* **Authentication** — JWT-based authentication protecting API resources

## Entities & Relationships

| Entity             | Relationship |
| ------------------ | ------------ |
| Category → Product | One-to-Many  |
| Supplier → Product | One-to-Many  |
| Customer → Sale    | One-to-Many  |
| User → Sale        | One-to-Many  |
| Sale → SaleItem    | One-to-Many  |
| Product → SaleItem | One-to-Many  |
| Sale → Payment     | One-to-Many  |
| Sale → Receipt     | One-to-One   |

Foreign keys are enforced at the database level and validated at the API level, returning clear errors such as `404 Not Found` for invalid references.

## Tech Stack

* **FastAPI** — API framework and routing
* **SQLAlchemy** — ORM and database layer
* **Pydantic** — request/response validation
* **PostgreSQL** — database
* **JWT + pwdlib** — authentication and password hashing

## Project Structure

```text
app/
├── main.py
├── database.py
├── core/              # Security and authentication
├── models/            # SQLAlchemy models
├── schemas/           # Pydantic schemas
├── repositories/      # Database operations
├── services/          # Business logic
└── routers/            # API endpoints
```

The application follows:

**Router → Service → Repository → Model**

## Setup

### 1. Install dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure PostgreSQL

Create a PostgreSQL database and add your connection details to `.env`:

```env
DATABASE_URL=postgresql+psycopg2://username:password@localhost:5432/your_database_name
SECRET_KEY=your-secret-key
```

### 3. Run the API

```bash
cd app
fastapi dev main.py
```

Tables are created automatically when the application starts.

### 4. Swagger Documentation

Open:

**[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**

Authentication is available through:

* `POST /auth/register` — create an account
* `POST /auth/login` — obtain a JWT access token
* `GET /auth/me` — view the authenticated user

Click **Authorize** in Swagger and enter the credentials to test protected endpoints.

## Error Handling

* **404** — resource or referenced foreign key does not exist
* **409** — resource cannot be deleted because it is referenced elsewhere
* **401** — authentication credentials are missing or invalid
* **422** — request data fails validation
