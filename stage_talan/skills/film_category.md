---
name: db_film_category
description: Stores the categorization of films in the database.
---

# Ground Truth: `film_category` Table

## 1. Schema & Column Definitions
- `film_id` (SMALLINT, PRIMARY KEY): Unique identifier for each film. Links to the film details in `film`.
- `category_id` (TINYINT, PRIMARY KEY): Unique identifier for each category. Links to the category details in `category`.
- `last_update` (TIMESTAMP, NOT NULL): Timestamp of the last update to the film-category relationship.

## 2. Relationships
- `film_id` → `film.film_id`: Links each film to its categorization.
- `category_id` → `category.category_id`: Links each category to its associated films.

## 3. Query Optimization & Constraints
- Join `film` and `category` on their respective IDs to retrieve film and category details.
- Use `last_update` with TIMESTAMP functions (NOW(), TIMESTAMPDIFF) for auditing and data quality checks.
- Filter by `category_id` to retrieve films belonging to a specific category.
- Group by `film_id` or `category_id` for aggregation queries on film categorization.