# Cron Synchronization Service

Incremental Odoo → PostgreSQL synchronization workers.

---

## Overview

This service is responsible for:

- Fetching updated records from Odoo
- Performing bulk upserts into PostgreSQL
- Maintaining synchronization state (`last_sync`)
- Running jobs sequentially

### How It Works

Each sync job follows this workflow:

1. Reads the last synchronization timestamp
2. Fetches updated records from Odoo
3. Bulk upserts records into the database
4. Updates the sync state
5. Commits the transaction

All jobs extend `BaseSyncJob`.

---

## Available Jobs

- **ContactsSyncJob** - Synchronizes contact records
- **InvoicesSyncJob** - Synchronizes invoice records

### Job Structure

Each job defines:

- `fetch(last_sync)` - Retrieves and parses Odoo data
- **Repository** - Handles bulk upsert logic

---

## Sync Strategy

- **Incremental sync** based on `write_date` - fetches all info from Odoo and keeps track of the latest `write_date` as reference
- **Conflict resolution** using PostgreSQL `ON CONFLICT`
- **Idempotent bulk upserts** - safe to run multiple times
- **Transactional commit/rollback** - ensures data consistency
