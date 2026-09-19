# POS (Point of Sale) API

A REST API for a small-to-medium retail business built with **FastAPI, SQLAlchemy, and PostgreSQL**. It manages inventory, customers, staff accounts, and sales.

## Features

- **Inventory Management** — categories, suppliers, products, stock, and pricing
- **Sales Processing** — sales, sale items, and multiple payment methods
- **Customer Management** — customer records linked to purchase history
- **User Access Control** — staff accounts with Admin and Cashier roles
- **Receipts** — unique receipt generated for each sale
- **Authentication** — JWT-based authentication protecting API resources

## Entities & Relationships

| Entity | Relationship |
|---|---|
| Category → Product | One-to-Many |
| Supplier → Product | One-to-Many |
| Customer → Sale | One-to-Many |
| User → Sale | One-to-Many |
| Sale → SaleItem | One-to-Many |
| Product → SaleItem | One-to-Many |
| Sale → Payment | One-to-Many |
| Sale → Receipt | One-to-One |

Foreign keys are enforced at the database level and validated at the API level, returning clear errors such as `404 Not Found` for invalid references.

## Tech Stack

- **FastAPI** — API framework and routing
- **SQLAlchemy** — ORM and database layer
- **Pydantic** — request/response validation
- **PostgreSQL** — database
- **JWT + pwdlib** — authentication and password hashing
- **Pytest** — automated testing
- **SQLite** — isolated test database

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
├── routers/           # API endpoints
└── tests/             # Automated tests