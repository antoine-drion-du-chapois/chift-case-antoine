# Antoine Chift Case

Odoo → PostgreSQL synchronization service with incremental cron jobs, REST API, automatic database initialization, and full Docker Compose orchestration.

---

## Production Deployment

**Live API:** http://34.77.28.170:8000/
**API DOC:** http://34.77.28.170:8000/docs

-> Auth info :  
"username": "admin",
"password": "admin"

### Authentication

The API uses **JWT authentication**. To access protected routes:

1. **Login** to obtain an access token:

   ```
   POST http://34.77.28.170:8000/auth/login
   ```

   **Request Body:**

   ```json
   {
     "username": "admin",
     "password": "admin"
   }
   ```

2. **Include the token** in subsequent requests via the `Authorization` header:
   ```
   Authorization: Bearer <your_token>
   ```

### Available Endpoints

```
GET http://34.77.28.170:8000/contacts/
GET http://34.77.28.170:8000/contacts/{id}
GET http://34.77.28.170:8000/invoices
GET http://34.77.28.170:8000/invoices/{id}
```

---

## Local Deployment

### Prerequisites

Create a `.env` file in the project root with the following variables:

```env
DATABASE_URL=
ODOO_URL=
ODOO_DB=
ODOO_USERNAME=
ODOO_PASSWORD=
SECRET_KEY=
SYNC_INTERVAL_MINUTES=
```

### Getting Started

Run the following command from the project root:

```bash
docker compose up --build
```

This will:

- Start PostgreSQL
- Initialize the database schema
- Launch cron synchronization jobs
- Start the API server

**Local API:** http://localhost:8000
