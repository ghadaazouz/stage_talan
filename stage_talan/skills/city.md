---
name: db_city
description: Stores information about cities including their names and corresponding countries.
---

# Ground Truth: `city` Table

## 1. Schema & Column Definitions
- `city_id` (SMALLINT, PRIMARY KEY): Unique identifier for each city.
- `city` (VARCHAR(50)): City name — e.g. "New York", "London", "Paris".
- `country_id` (SMALLINT, FK): Country identifier. Join with `country.country_id` to get the country name.
- `last_update` (TIMESTAMP): Timestamp of the last update to the city record.

## 2. Relationships
- `country_id` → `country.country_id`: Links each city to its corresponding country.

## 3. Query Optimization & Constraints
- Join `country` on `country_id` to retrieve country names in aggregation queries.
- Use `last_update` with TIMESTAMP functions (NOW(), TIMESTAMPDIFF) for data freshness analysis.
- Filter by `city` or `country_id` to retrieve cities within a specific region.
- Group by `country_id` (not `country_name`) for better index performance.