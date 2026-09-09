---
name: db_film_text
description: Stores detailed information about each film including title and description.
---

# Ground Truth: `film_text` Table

## 1. Schema & Column Definitions
- `film_id` (SMALLINT, PRIMARY KEY): Unique identifier for each film. Auto-incremented.
- `title` (VARCHAR(255), NOT NULL): Film title — the primary name of the movie or TV episode.
- `description` (TEXT): Brief summary or description of the film. May be empty for some titles.

## 2. Relationships
None

## 3. Query Optimization & Constraints
- Use `title` with LIKE or CONTAINS for searching film titles.
- Filter by `description` using CONTAINS or MATCH for text-based queries.
- Group by `film_id` for aggregation queries on film-level data.
- Consider indexing `title` for faster title-based searches.