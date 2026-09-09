---
name: db_language
description: Stores information about supported languages including name and last update timestamp.
---

# Ground Truth: `language` Table

## 1. Schema & Column Definitions
- `language_id` (TINYINT, PRIMARY KEY): Unique identifier for each language (e.g. 1 for English).
- `name` (CHAR(20), NOT NULL): Language name — e.g. 'English', 'Spanish', 'French'.
- `last_update` (TIMESTAMP, NOT NULL): Timestamp of the last update to the language record.

## 2. Relationships
None

## 3. Query Optimization & Constraints
- Use `name` with LIKE operator for language filtering (e.g. '%English%').
- Filter by `last_update` to retrieve languages updated within a specific time range.
- Group by `language_id` for aggregation queries (e.g. count of languages).
- Consider indexing `last_update` for efficient date-based queries.