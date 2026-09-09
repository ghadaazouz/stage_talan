---
name: db_address
description: Stores physical addresses for customers, employees, or other entities.
---

# Ground Truth: `address` Table

## 1. Schema & Column Definitions
- `address_id` (SMALLINT, PRIMARY KEY): Unique identifier for each address.
- `address` (VARCHAR(50), NOT NULL): Street address or physical location.
- `address2` (VARCHAR(50)): Additional address information (e.g. apartment number, suite).
- `district` (VARCHAR(20), NOT NULL): Neighborhood or postal district.
- `city_id` (SMALLINT, FK, NOT NULL): City identifier. Join with `city.city_id` to get the city name.
- `postal_code` (VARCHAR(10)): Postal code or zip code for mail delivery.
- `phone` (VARCHAR(20), NOT NULL): Phone number associated with the address.
- `location` (NULL, NOT NULL): Inferred to be a geographic location (latitude, longitude) — always NULL in this table.
- `last_update` (TIMESTAMP, NOT NULL): Timestamp for the last update to the address record.

## 2. Relationships
- `city_id` → `city.city_id`: Links each address to its city.

## 3. Query Optimization & Constraints
- Join `city` on `city_id` to retrieve city names in aggregation queries.
- Use `address` and `address2` together to construct full addresses for mailings.
- Filter by `district` or `postal_code` for location-based queries.
- Always join `city` via `city_id` to enrich addresses with city names.
- Consider creating a separate table for geographic locations (latitude, longitude) if needed.