---
name: db_payment
description: Stores payment information for customer rentals including amount and date.
---

# Ground Truth: `payment` Table

## 1. Schema & Column Definitions
- `payment_id` (SMALLINT, PRIMARY KEY): Unique identifier for each payment record.
- `customer_id` (SMALLINT, FK): Customer identifier. Join with `customer.customer_id` for customer details.
- `staff_id` (TINYINT, FK): Staff identifier. Join with `staff.staff_id` for staff details.
- `rental_id` (INTEGER, FK): Rental identifier. Join with `rental.rental_id` for rental details.
- `amount` (DECIMAL(5, 2)): Payment amount including any applicable taxes.
- `payment_date` (DATETIME): Date the payment was made. Use for time-based analysis.
- `last_update` (TIMESTAMP): Timestamp of the last update to this payment record.

## 2. Relationships
- `customer_id` → `customer.customer_id`: Links each payment to the customer who made it.
- `rental_id` → `rental.rental_id`: Links each payment to the rental it is associated with.
- `staff_id` → `staff.staff_id`: Links each payment to the staff member who processed it.

## 3. Query Optimization & Constraints
- Join `customer`, `rental`, and `staff` tables via their respective IDs to enrich payments with customer, rental, and staff details.
- Filter `payment_date` using DATE functions (MONTH, YEAR) for time-based analysis.
- Sum `amount` grouped by `customer_id` or `rental_id` for aggregation queries.
- Use `last_update` to track changes to payment records over time.