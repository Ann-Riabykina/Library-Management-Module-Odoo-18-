# Library Management Module (Odoo 18)

## Overview

This module implements a simple library management system for Odoo 18.

It allows:

* Managing books
* Renting books to partners
* Preventing double renting
* Returning books
* Checking availability status
* Accessing books via REST API

---

## Features

### Models

#### `library.book`

* `name` – Book title (required)
* `author` – Author
* `published_date` – Publication date
* `is_available` – Availability status (default = True)

#### `library.rent`

* `partner_id` – Reader (res.partner)
* `book_id` – Book
* `rent_date` – Auto-filled on creation
* `return_date` – Return date (optional)

### Business Logic

* A book cannot be rented twice until returned.
* Issuing a book sets `is_available = False`.
* Returning a book sets `is_available = True`.

### Wizard

Button **"Issue Book"**:

* Opens wizard
* Select reader
* Creates rent record (`library.rent`)

### Return Action

Button **"Return Book"**:

* Marks book as returned (sets `return_date` to today)
* Automatically updates availability

### REST API

Endpoint:

GET `/library/books`

Returns JSON list of all books with availability.

> Note: The endpoint is implemented as `auth="public"` + `sudo()` for the test task.
> In a real project you would typically require authentication/authorization.

---

## Installation (Docker / docker-compose)

### 1) Start Odoo 18 + Postgres

Example minimal `docker-compose.yml` (adapt paths/versions if you already have one):

```yaml
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: test_odoo
      POSTGRES_USER: odoo
      POSTGRES_PASSWORD: odoo
  odoo:
    image: odoo:18
    depends_on:
      - db
    ports:
      - "8069:8069"
    environment:
      HOST: db
      USER: odoo
      PASSWORD: odoo
    volumes:
      - ./extra-addons:/mnt/extra-addons
```

Then run:

```bash
docker compose up -d
```

### 2) Put the module into addons

Copy `library_management/` into:

`./extra-addons/library_management/`

### 3) Create DB and install the module

1. Open Odoo in browser: `http://localhost:8069`
2. Create database: **test_odoo**
3. Apps → **Update Apps List**
4. Install **Library Management**

### 4) Enable Developer Mode (for technical menus)

Settings → scroll down → **Activate the developer mode**.

---

## Usage

1. Create a book (Library → Books).
2. Click **Issue Book**.
3. Select a reader.
4. Confirm rent (a `library.rent` record is created).
5. Use **Return Book** on the rent record to return it.

---

## Quick API check

```bash
curl -s http://localhost:8069/library/books | jq .
```
