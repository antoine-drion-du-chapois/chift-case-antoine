# Cron Synchronization Service

Incremental Odoo → PostgreSQL synchronization workers.

This service is responsible for:

- Fetching updated records from Odoo
- Performing bulk upserts into PostgreSQL
- Maintaining synchronization state (`last_sync`)
- Running jobs sequentially

---

## Overview

Each sync job:

1. Reads the last synchronization timestamp
2. Fetches updated records from Odoo
3. Bulk upserts records into the database
4. Updates the sync state
5. Commits the transaction

All jobs extend `BaseSyncJob`.

---

## Available Jobs

- `ContactsSyncJob`
- `InvoicesSyncJob`

Each job defines:

- `fetch(last_sync)` → Retrieves and parses Odoo data
- Repository → Handles bulk upsert logic

## Sync Strategy

- Incremental sync based on `write_date`, fetches all the info from odoo and keeps track of the latest 'write_date' and keeps it as reference
- Conflict resolution using PostgreSQL `ON CONFLICT`
- Idempotent bulk upserts
- Transactional commit / rollback
