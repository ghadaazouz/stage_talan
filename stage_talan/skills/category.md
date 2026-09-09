---
name: db_category
description: Stores a list of product categories with their names and last update timestamps.
---

# Ground Truth: `category` Table

## 1. Schema & Column Definitions
- `category_id` (TINYINT, PRIMARY KEY): Unique identifier for each product category.
- `name` (VARCHAR(25)): Category name — e.g. "Electronics", "Clothing", etc.
- `last_update` (TIMESTAMP): Timestamp of the last update to the category record.

## 2. Relationships
- None

## 3. Query Optimization & Constraints
- Use `name` for filtering or grouping by category type.
- Join with other tables via `category_id` to retrieve products belonging to each category.
- Use `last_update` with TIMESTAMP functions (NOW(), TIMESTAMPDIFF) for data freshness analysis.
- Consider indexing `name` for faster filtering and grouping operations.