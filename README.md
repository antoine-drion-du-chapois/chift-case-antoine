<!-- prettier-ignore -->
# Antoine Chift Case

Odoo → PostgreSQL synchronization service with:

- Incremental cron jobs
- REST API
- Automatic database initialization
- Fully orchestrated via Docker Compose

---

## Environment Variables

A `.env` file **must** be present at the project root with the following variables:

```env
DATABASE_URL=
ODOO_URL=
ODOO_DB=
ODOO_USERNAME=
ODOO_PASSWORD=
SECRET_KEY=
SYNC_INTERVAL_MINUTES=
```

## Getting Started

From the project root:

```bash
docker compose up --build
```

This command will:

- Start PostgreSQL
- Initialize the database schema
- Launch the cron synchronization jobs
- Start the API server

## URL

Api available at : http://localhost:8000
