# Sellers Micro Service

A small FastAPI micro service that manages **sellers** and the **items** they offer.
It is one half of a two-service learning project and is consumed over HTTP by the
companion [`customer_micro_service`](https://github.com/IlaiTayar/customer_micro_service),
which looks up item prices and validates favorite items against this service.

> This is a personal learning project built to practice a layered micro service
> architecture (REST API + MySQL + Redis caching). It is not meant for production use.

## Features

- CRUD for **sellers**, each with an `active` / `inactive` status.
- CRUD for **items**, each belonging to a seller.
- Lookup of an item by name returning the **lowest-priced** match (used by the customer
  service when pricing orders).
- **Cross-service reference checks**: before deleting a seller or an item, the service asks
  the customer service whether the item is still referenced by customer orders or favorites.
  Deletion is blocked (`409`) while references exist. If the customer service is
  unavailable the delete request fails with `503` so no unverified deletion happens.
- **Redis** caching for item-by-id reads, with a configurable TTL.

## Tech stack

- Python 3.11+
- [FastAPI](https://fastapi.tiangolo.com/) + [Uvicorn](https://www.uvicorn.org/)
- [`databases`](https://www.encode.io/databases/) + `aiomysql` (async MySQL access)
- [Pydantic v2](https://docs.pydantic.dev/) + `pydantic-settings`
- [Redis](https://redis.io/) via `redis-py`

## Architecture

The service follows a clean, layered structure:

```
controller/   FastAPI routers (HTTP layer, request/response + error mapping)
service/      Business logic / validation
repository/   Data access (SQL queries + Redis cache)
model/        Pydantic domain models (Seller, Item)
config/       Settings loaded from environment variables
```

## Project layout

```
sellers_micro_service/
├─ main.py                      # FastAPI app + startup/shutdown (lifespan)
├─ database.py                  # Async Database instance
├─ config/config.py             # Settings (env-driven)
├─ controller/                  # seller / item routers
├─ service/                     # business logic
├─ repository/                  # SQL + cache access
├─ model/                       # pydantic models (Seller, Item)
├─ redisClient/redis_client.py  # Redis client
├─ resources/db-migrations/     # init.sql (schema + seed data)
├─ docker-compose.yml           # MySQL + Redis for local development
└─ requirements.txt
```

## Configuration

All settings have defaults and can be overridden with environment variables
(see `config/config.py`):

| Variable         | Default      | Description          |
|------------------|--------------|----------------------|
| `MYSQL_USER`     | `user`       | MySQL user           |
| `MYSQL_PASSWORD` | `password`   | MySQL password       |
| `MYSQL_HOST`     | `localhost`  | MySQL host           |
| `MYSQL_PORT`     | `3307`       | MySQL port           |
| `MYSQL_DATABASE` | `main`       | Database name        |
| `REDIS_HOST`     | `localhost`  | Redis host           |
| `REDIS_PORT`     | `6380`       | Redis port           |
| `REDIS_TTL`      | `100`        | Cache TTL in seconds |

The SQLAlchemy-style `DATABASE_URL` is derived automatically from the `MYSQL_*` values.

> Note: this service uses ports `3307` (MySQL) and `6380` (Redis) so it can run
> side-by-side with the customer service, which uses `3306` and `6379`.

## Getting started

### 1. Start MySQL and Redis

```bash
docker compose up -d
```

This starts a MySQL 8 instance on `3307` (seeded from `resources/db-migrations/init.sql`)
and a Redis instance on `6380`.

### 2. Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Run the service

The customer service expects this one on port `8001`:

```bash
uvicorn main:app --reload --port 8001
```

Interactive API docs are then available at `http://localhost:8001/docs`.

## API overview

### Sellers (`/seller`)

| Method | Path                    | Description             |
|--------|-------------------------|-------------------------|
| POST   | `/seller/create`        | Create a seller         |
| PUT    | `/seller/update-{id}`   | Update a seller by id   |
| GET    | `/seller/get-{id}`      | Get a seller by id      |
| GET    | `/seller/get/all`       | List all sellers        |
| DELETE | `/seller/{id}`          | Delete a seller by id   |

> Deleting a seller cascades to its items, but is blocked with `409` if any of those items
> are still referenced by customer orders or favorites (checked via the customer service).
> The seller is notified in that case and nothing is deleted.

### Items (`/item`)

| Method | Path                       | Description                               |
|--------|----------------------------|-------------------------------------------|
| POST   | `/item/create`             | Create an item                            |
| PUT    | `/item/update-{id}`        | Update an item by id                      |
| GET    | `/item/get-id-{id}`        | Get an item by id                         |
| GET    | `/item/get-name-{name}`    | Get the lowest-priced item with that name |
| GET    | `/item/get-all`            | List all items                            |
| DELETE | `/item/delete-{id}`        | Delete an item by id                      |

> Deleting an item is blocked with `409 ITEM_IN_USE` if it is still referenced by customer
> orders or favorites. These reference checks call the customer service; if that service is
> unavailable the request fails with `503`.

### Example

```bash
curl -X POST http://localhost:8001/item/create \
  -H "Content-Type: application/json" \
  -d '{"seller_id": 1, "item_name": "Laptop", "price": 999.99}'
```
