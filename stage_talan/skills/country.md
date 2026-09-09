---
name: db_country
description: Stores information about countries including their names and last update timestamps.
---

# Ground Truth: `country` Table

## 1. Schema & Column Definitions
- `country_id` (SMALLINT, PRIMARY KEY): Unique identifier for each country.
- `country` (VARCHAR(50)): Country name — e.g. "United States", "Canada", "Mexico".
- `last_update` (TIMESTAMP): Timestamp of the last update to the country record.

## 2. Relationships
- None

## 3. Query Optimization & Constraints
- Use `country_id` for efficient joins with other tables.
- Filter by `country` when retrieving specific countries for reporting.
- Use `last_update` with DATE functions (MONTH, YEAR) for data freshness analysis.
- Consider indexing `country` for faster string matching queries.