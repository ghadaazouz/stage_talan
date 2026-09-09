---
name: db_inventory
description: Stores inventory information for each film stocked in each store.
---

# Ground Truth: `inventory` Table

## 1. Schema & Column Definitions
- `inventory_id` (MEDIUMINT, PRIMARY KEY): Unique identifier for each inventory record.
- `film_id` (SMALLINT, FK): Film identifier. Join with `film.film_id` to get the film title and details.
- `store_id` (TINYINT, FK): Store identifier. Join with `store.store_id` to get the store name and address.
- `last_update` (TIMESTAMP): Timestamp of the last inventory update. Use to track changes and compute inventory age.

## 2. Relationships
- `film_id` → `film.film_id`: Links each inventory record to the corresponding film.
- `store_id` → `store.store_id`: Links each inventory record to the corresponding store.

## 3. Query Optimization & Constraints
- Join `film` and `store` on `film_id` and `store_id` respectively to retrieve film and store information.
- Filter by `last_update` to track inventory changes over time.
- Group by `film_id` or `store_id` for aggregation queries (e.g., total inventory count per film or store).
- Use `last_update` with TIMESTAMP functions (NOW(), TIMESTAMPDIFF) for inventory aging analysis.