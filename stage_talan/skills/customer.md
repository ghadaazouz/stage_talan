---
name: db_customer
description: Stores customer information including contact details, store association, and account status.
---

# Ground Truth: `customer` Table

## 1. Schema & Column Definitions
- `customer_id` (SMALLINT, PRIMARY KEY): Unique identifier for each customer.
- `store_id` (TINYINT): Store identifier where the customer is associated. Join with `store.store_id` to get the store name.
- `first_name` (VARCHAR(45)): Customer's first name.
- `last_name` (VARCHAR(45)): Customer's last name.
- `email` (VARCHAR(50)): Customer's email address.
- `address_id` (SMALLINT, FK): Address identifier. Join with `address.address_id` to get the address details.
- `active` (TINYINT): Active flag — 1 = active, 0 = inactive/deactivated. Always filter WHERE active = 1 for current customer count.
- `create_date` (DATETIME): Date when the customer account was created.
- `last_update` (TIMESTAMP): Timestamp of the last update to the customer record.

## 2. Relationships
- `address_id` → `address.address_id`: Links each customer to their address.
- `store_id` → `store.store_id`: Links each customer to their associated store.

## 3. Query Optimization & Constraints
- Always filter `WHERE active = 1` to exclude deactivated customers.
- Join `address` on `address_id` to retrieve address details in aggregation queries.
- Join `store` on `store_id` to retrieve store names in aggregation queries.
- Use `create_date` with DATE functions (MONTH, YEAR) for customer acquisition analysis.