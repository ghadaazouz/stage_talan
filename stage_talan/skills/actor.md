---
name: db_actor
description: Stores information about actors in a movie database.
---

# Ground Truth: `actor` Table

## 1. Schema & Column Definitions
- `actor_id` (SMALLINT, PRIMARY KEY): Unique identifier for each actor.
- `first_name` (VARCHAR(45), NOT NULL): Actor's first name.
- `last_name` (VARCHAR(45), NOT NULL): Actor's last name.
- `last_update` (TIMESTAMP, NOT NULL): Timestamp of the last update to the actor's record.

## 2. Relationships
None

## 3. Query Optimization & Constraints
- Use `first_name` and `last_name` for actor name searches and filtering.
- Filter by `last_update` to retrieve actors with recent updates.
- Group by `actor_id` for aggregation queries (e.g., average number of movies per actor).
- Consider indexing `last_update` for efficient filtering by timestamp.