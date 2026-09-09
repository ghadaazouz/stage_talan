import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

DB_URL = (
    f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

engine = create_engine(DB_URL)


def execute(sql: str) -> dict:
    """
    Exécute une requête SQL en lecture seule.
    Retourne les colonnes + les lignes + le nombre de résultats.

    Args:
        sql : requête SELECT validée par le SQL Validator

    Returns:
        dict avec columns, rows, row_count
    """
    try:
        with engine.connect() as conn:
            result = conn.execute(text(sql))
            columns = list(result.keys())
            rows    = [dict(row._mapping) for row in result.fetchall()]

        return {
            "status":    "success",
            "columns":   columns,
            "rows":      rows,
            "row_count": len(rows)
        }

    except Exception as e:
        return {
            "status": "error",
            "error":  str(e),
            "columns": [],
            "rows":    [],
            "row_count": 0
        }


if __name__ == "__main__":

    test_queries = [
        {
            "question": "How many actors?",
            "sql": "SELECT COUNT(actor_id) AS total_actors FROM actor"
        },
        {
            "question": "Show me all movies released this year",
            "sql": "SELECT film_id, title, release_year FROM film WHERE release_year = YEAR(CURDATE()) LIMIT 10"
        }
    ]

    print("SQL Executor — Test\n")

    for case in test_queries:
        print(f"Q  : {case['question']}")
        print(f"SQL: {case['sql']}")
        result = execute(case["sql"])
        print(f"   status    : {result['status']}")
        print(f"   row_count : {result['row_count']}")
        print(f"   columns   : {result['columns']}")
        if result["rows"]:
            print(f"   rows      :")
            for row in result["rows"][:3]:   # affiche max 3 lignes
                print(f"      {row}")
        print()
