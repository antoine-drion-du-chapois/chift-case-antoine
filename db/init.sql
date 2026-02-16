CREATE TABLE contacts (
    id SERIAL PRIMARY KEY,
    odoo_id INTEGER UNIQUE NOT NULL,
    name TEXT,
    email TEXT,
    active BOOLEAN,
    write_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
);

CREATE TABLE invoices (
    id SERIAL PRIMARY KEY,
    odoo_id INTEGER UNIQUE NOT NULL,
    name TEXT,
    amount_total NUMERIC(12, 2) NOT NULL,
    invoice_date DATE,
    write_date TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP DEFAULT NOW() NOT NULL,
);


CREATE TABLE sync_state (
    job_name TEXT PRIMARY KEY,
    last_sync TIMESTAMP NOT NULL
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL
);


INSERT INTO sync_state (job_name, last_sync)
VALUES ('contacts_sync', '1970-01-01 00:00:00');

INSERT INTO sync_state (job_name, last_sync)
VALUES ('invoices_sync', '1970-01-01 00:00:00');

INSERT INTO users (username, hashed_password)
VALUES (
    'admin',
    '$2a$12$1AflYuKf2kgJBvlRVd4nMOUHn5jr4T6Kg4jqHBS2yD6Vu1RyhyP0.' 
)
ON CONFLICT (username) DO NOTHING;
