---
name: db_store
description: Stores information about each retail store including its manager and address.
---

# Ground Truth: `store` Table

## 1. Schema & Column Definitions
- `store_id` (TINYINT, PRIMARY KEY): Unique identifier for each retail store.
- `manager_staff_id` (TINYINT, FK): Staff identifier of the store manager. Join with `staff.staff_id` to get the manager's details.
- `address_id` (SMALLINT, FK): Address identifier. Join with `address.address_id` to get the store's physical address.
- `last_update` (TIMESTAMP): Timestamp of the last update to the store's information.

## 2. Relationships
- `address_id` → `address.address_id`: Links each store to its physical address.
- `manager_staff_id` → `staff.staff_id`: Links each store to its manager.

## 3. Query Optimization & Constraints
- Join `address` on `address_id` to retrieve the store's address in aggregation queries.
- Join `staff` on `manager_staff_id` to enrich store data with manager information.
- Use `last_update` with TIMESTAMP functions (NOW(), TIMESTAMPDIFF) for data freshness analysis.
- Filter by `store_id` when retrieving data for a specific store.