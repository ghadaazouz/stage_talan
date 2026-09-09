---
name: db_film_actor
description: Stores the many-to-many relationships between actors and films in the movie catalog.
---

# Ground Truth: `film_actor` Table

## 1. Schema & Column Definitions
- `actor_id` (SMALLINT, PRIMARY KEY, FK): Unique identifier for each actor. Join with `actor.actor_id` for actor details.
- `film_id` (SMALLINT, PRIMARY KEY, FK): Unique identifier for each film. Join with `film.film_id` for film details.
- `last_update` (TIMESTAMP, NOT NULL): Timestamp of the last update to the actor-film relationship. Inferred.

## 2. Relationships
- `actor_id` → `actor.actor_id`: Links each actor to their film roles.
- `film_id` → `film.film_id`: Links each film to its cast of actors.

## 3. Query Optimization & Constraints
- Join `actor` and `film` on `actor_id` and `film_id` respectively to retrieve actor and film details.
- Use `last_update` with TIMESTAMP functions (NOW(), TIMESTAMPDIFF) for auditing or data quality checks.
- Filter by `actor_id` or `film_id` to retrieve a specific actor's filmography or a film's cast.
- Group by `actor_id` or `film_id` for aggregation queries on actor or film performance metrics.