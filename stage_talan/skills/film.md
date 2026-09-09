---
name: db_film
description: Stores information about all films available for rental, including title, description, and rental details.
---

# Ground Truth: `film` Table

## 1. Schema & Column Definitions
- `film_id` (SMALLINT, PRIMARY KEY): Unique identifier for each film.
- `title` (VARCHAR(128), NOT NULL): Film title — the primary name of the movie.
- `description` (TEXT): Brief description of the film — use for marketing or cataloging.
- `release_year` (YEAR): Year the film was released. Use for historical analysis or filtering by era.
- `language_id` (TINYINT, NOT NULL): Language of the film. Join with `language.language_id` to get the language name.
- `original_language_id` (TINYINT): Original language of the film. Inferred, as it's unclear why this is separate from `language_id`.
- `rental_duration` (TINYINT, NOT NULL): Number of days a film can be rented. Use for calculating revenue or inventory management.
- `rental_rate` (DECIMAL(4, 2), NOT NULL): Daily rental rate for the film. Use for pricing or revenue analysis.
- `length` (SMALLINT): Film length in minutes. Inferred, as it's unclear why this is stored separately from `rental_duration`.
- `replacement_cost` (DECIMAL(5, 2), NOT NULL): Cost to replace a damaged film. Use for inventory management or financial analysis.
- `rating` (ENUM): Film rating — 'G', 'PG', 'PG-13', 'R', 'NC-17'. Use for filtering by audience or content.
- `special_features` (SET): Special features available for the film — 'Trailers', 'Commentaries', 'Deleted Scenes', etc. Inferred, as it's unclear what these values represent.
- `last_update` (TIMESTAMP, NOT NULL): Timestamp of the last update to the film record. Use for auditing or data quality analysis.

## 2. Relationships
- `language_id` → `language.language_id`: Links each film to its language.
- `original_language_id` → `language.language_id`: Links each film to its original language (inferred).

## 3. Query Optimization & Constraints
- Filter by `rating` to exclude films not suitable for a particular audience.
- Use `release_year` with YEAR() or DATE_FORMAT() for historical analysis or filtering by era.
- Join `language` on `language_id` to retrieve language names for aggregation queries.
- Group by `language_id` (not `language_name`) for better index performance.
- Use `rental_duration` and `rental_rate` to calculate revenue or inventory management metrics.