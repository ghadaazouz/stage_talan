---
name: db_staff
description: Stores information about all staff members including personal details, address, and store assignments.
---

# Ground Truth: `staff` Table

## 1. Schema & Column Definitions
- `staff_id` (TINYINT, PRIMARY KEY): Unique identifier for each staff member.
- `first_name` (VARCHAR(45), NOT NULL): Staff member's first name.
- `last_name` (VARCHAR(45), NOT NULL): Staff member's last name.
- `address_id` (SMALLINT, FK): Address identifier. Join with `address.address_id` to get the staff member's address.
- `picture` (BLOB): Staff member's profile picture (binary data).
- `email` (VARCHAR(50)): Staff member's email address.
- `store_id` (TINYINT, FK): Store identifier. Join with `store.store_id` to get the store where the staff member is assigned.
- `active` (TINYINT, NOT NULL): Active flag — 1 = active, 0 = inactive. Always filter WHERE active = 1 for current staff count.
- `username` (VARCHAR(16), NOT NULL): Staff member's username for login purposes.
- `password` (VARCHAR(40) COLLATE "utf8mb4_bin", NOT NULL): Staff member's password (hashed for security).
- `last_update` (TIMESTAMP, NOT NULL): Timestamp of the last update to the staff member's record.

## 2. Relationships
- `address_id` → `address.address_id`: Links each staff member to their address.
- `store_id` → `store.store_id`: Links each staff member to their assigned store.

## 3. Query Optimization & Constraints
- Always filter `WHERE active = 1` to exclude inactive staff members.
- Join `address` on `address_id` to retrieve staff member addresses in aggregation queries.
- Join `store` on `store_id` to retrieve store names in aggregation queries.
- Use `last_update` with TIMESTAMP functions (NOW(), TIMESTAMPDIFF) for auditing and data quality checks.