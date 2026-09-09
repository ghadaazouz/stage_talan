---
name: db_rental
description: Stores information about each rental transaction including dates and staff involved.
---

# Ground Truth: `rental` Table

## 1. Schema & Column Definitions
- `rental_id` (INTEGER, PRIMARY KEY): Unique identifier for each rental transaction.
- `rental_date` (DATETIME, NOT NULL): Date the rental started. Use to filter by rental period or compute rental duration.
- `inventory_id` (MEDIUMINT, FK): Inventory identifier. Join with `inventory.inventory_id` to get the rented item details.
- `customer_id` (SMALLINT, FK): Customer identifier. Join with `customer.customer_id` to get the customer details.
- `return_date` (DATETIME): Date the rental ended. Inferred to be NULL for ongoing rentals.
- `staff_id` (TINYINT, FK): Staff identifier. Join with `staff.staff_id` to get the staff member involved in the rental.
- `last_update` (TIMESTAMP, NOT NULL): Timestamp of the last update to the rental record.

## 2. Relationships
- `inventory_id` → `inventory.inventory_id`: Links each rental to the rented item.
- `customer_id` → `customer.customer_id`: Links each rental to the customer who rented it.
- `staff_id` → `staff.staff_id`: Links each rental to the staff member involved in the rental.

## 3. Query Optimization & Constraints
- Filter `WHERE return_date IS NULL` to retrieve ongoing rentals.
- Use `rental_date` with DATE functions (MONTH, YEAR) for rental period analysis.
- Join `inventory`, `customer`, and `staff` on their respective IDs to retrieve item, customer, and staff details in aggregation queries.
- Group by `inventory_id` (not `inventory_name`) for better index performance.