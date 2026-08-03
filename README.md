# POS (Point of Sale) API

A REST API for a small-to-medium retail business, built with **FastAPI**, **SQLAlchemy**, and **PostgreSQL**. It manages inventory, customers, staff accounts, and sales transactions.

## Features

- **Inventory Management** — categories, suppliers, and products with stock/pricing data
- **Sales Processing** — sales, line items (sale items), and payments, including support for multiple payment methods
- **Customer Relationship Management** — customer contact records linked to purchase history
- **User Access Control** — staff accounts with role-based access (Admin, Cashier)
- **Receipts** — a unique receipt generated per sale

## Entities & Relationships

| Entity | Relationship |
|---|---|
| Category → Product | One-to-Many |
| Supplier → Product | One-to-Many |
| Customer → Sale | One-to-Many (customer is optional on a sale) |
| User → Sale | One-to-Many |
| Sale → SaleItem | One-to-Many |
| Product → SaleItem | One-to-Many |
| Sale → Payment | One-to-Many |
| Sale → Receipt | One-to-One |

All relationships are enforced at the database level via SQLAlchemy foreign keys, and validated at the API level before insert/update — for example, creating a `SaleItem` with a `product_id` that doesn't exist returns a `404`, not a database error.

## Tech Stack

- **FastAPI** — web framework and routing
- **SQLAlchemy** — ORM and database layer
- **Pydantic** — request/response validation
- **PostgreSQL** — database

## Project Structure

```
app/
├── main.py                # App entrypoint, wires up all routers
├── database.py             # Engine, session, and Base setup
├── models/                 # SQLAlchemy ORM models (one file per entity)
├── schemas/                 # Pydantic request/response schemas
├── repositories/            # Data-access layer (raw DB operations)
├── services/                 # Business logic layer (validation, 404s, FK checks)
└── routers/                  # FastAPI route definitions (one router per entity)
```

Each entity follows the same layered pattern: **router → service → repository → model**. Routers only depend on services; services own all business rules (not-found handling, foreign key validation, conflict handling on delete); repositories only talk to the database.

## Setup

### 1. Install dependencies

```bash
python3 -m venv venv
source venv/bin/activate      # on Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Set up PostgreSQL

Create a database matching the connection string in `app/database.py`:

```bash
createdb -h localhost -U postgres pos_db
```

## Configuration

Create a `.env` file in the project root with:

```env
DATABASE_URL=postgresql+psycopg2://username:password@localhost:5432/your_database_name
```

### 3. Run the app

```bash
cd app
fastapi dev main.py
```

Tables are created automatically on startup via `Base.metadata.create_all`.

### 4. Explore the API

Open **http://127.0.0.1:8000/docs** for the Swagger UI, where every entity supports:

- `POST   /entity/`        — create a record
- `GET    /entity/`        — list all records
- `GET    /entity/{id}`    — retrieve a single record
- `PUT    /entity/{id}`    — update a record
- `DELETE /entity/{id}`    — delete a record

Available resources: `/categories`, `/suppliers`, `/products`, `/customers`, `/users`, `/sales`, `/sale-items`, `/payments`, `/receipts`.

## Error Handling

- **404 Not Found** — requesting, updating, or deleting a record that doesn't exist, or creating/updating a record with a foreign key that points at a nonexistent row (e.g. a sale item referencing a product that isn't in the database)
- **409 Conflict** — attempting to delete a record that's still referenced by other records (e.g. deleting a product that appears in an existing sale item)
- **422 Unprocessable Entity** — request body fails Pydantic validation (missing required fields, wrong types, etc.)
