import re


# ─────────────────────────────────────────
#  SQL Validator — 100% local, sans LLM
#  Le LLM ne voit jamais les données
# ─────────────────────────────────────────

# Mots interdits — toute requête qui commence par ces mots est bloquée
FORBIDDEN_KEYWORDS = [
    "INSERT", "UPDATE", "DELETE", "DROP", "ALTER",
    "CREATE", "TRUNCATE", "REPLACE", "GRANT", "REVOKE"
]

# Patterns suspects — injection SQL classique
INJECTION_PATTERNS = [
    r"(--|#|/\*)",           # commentaires SQL
    r";\s*\w+",              # plusieurs statements (SELECT ...; DROP ...)
    r"'\s*OR\s*'",           # ' OR '1'='1
    r"SLEEP\s*\(",           # SLEEP(5)
    r"BENCHMARK\s*\(",       # BENCHMARK(...)
    r"LOAD_FILE\s*\(",       # LOAD_FILE(...)
    r"INTO\s+OUTFILE",       # SELECT INTO OUTFILE
    r"INFORMATION_SCHEMA",   # accès aux métadonnées système
]


def validate(sql: str, available_tables: list) -> dict:
    """
    Valide la requête SQL générée avant exécution.

    Args:
        sql              : requête SQL générée par le SQL Generation Agent
        available_tables : liste des tables autorisées (depuis le Detection Agent)

    Returns:
        dict avec status, risk_level, errors, sql_clean
    """
    errors = []
    sql_clean = sql.strip().rstrip(";")  # retire le ; final si présent

    # ── 1. Doit commencer par SELECT ──────────────────────────────
    first_word = sql_clean.split()[0].upper() if sql_clean else ""
    if first_word != "SELECT":
        errors.append(f"FORBIDDEN: query starts with '{first_word}' — only SELECT allowed")

    # ── 2. Mots clés interdits dans la requête ────────────────────
    sql_upper = sql_clean.upper()
    for keyword in FORBIDDEN_KEYWORDS:
        # regex pour matcher le mot entier (pas "SELECTALL" etc)
        if re.search(rf'\b{keyword}\b', sql_upper):
            errors.append(f"FORBIDDEN keyword detected: {keyword}")

    # ── 3. Patterns d'injection SQL ───────────────────────────────
    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, sql_clean, re.IGNORECASE):
            errors.append(f"INJECTION pattern detected: {pattern}")

    # ── 4. Tables utilisées dans la requête ───────────────────────
    # Extrait les noms après FROM et JOIN
    from_tables = re.findall(
        r'(?:FROM|JOIN)\s+`?(\w+)`?', sql_clean, re.IGNORECASE
    )
    unauthorized = [t for t in from_tables if t not in available_tables]
    if unauthorized:
        errors.append(f"UNAUTHORIZED tables: {unauthorized} — not detected by Detection Agent")

    # ── 5. Calcul du niveau de risque ─────────────────────────────
    if errors:
        risk_level = "HIGH"
        status = "REJECTED"
    elif len(from_tables) > 3:
        risk_level = "MEDIUM"   # jointures complexes — montrer à l'utilisateur
        status = "VALIDATED"
    else:
        risk_level = "LOW"
        status = "VALIDATED"

    return {
        "status":      status,
        "risk_level":  risk_level,
        "errors":      errors,
        "sql_clean":   sql_clean,
        "tables_used": from_tables
    }


def print_result(question, sql, result):
    print(f"Q  : {question}")
    print(f"SQL: {sql}")
    print(f"   status     : {result['status']}")
    print(f"   risk_level : {result['risk_level']}")
    print(f"   tables     : {result['tables_used']}")
    if result["errors"]:
        for e in result["errors"]:
            print(f"   ✗ {e}")
    else:
        print(f"   ✓ No issues found")
    print()


if __name__ == "__main__":

    print("SQL Validator — Test\n")

    # ── Cas 1 : requête valide ─────────────────────────────────────
    print_result(
        question="How many actors?",
        sql="SELECT COUNT(actor_id) AS total_actors FROM actor",
        result=validate(
            sql="SELECT COUNT(actor_id) AS total_actors FROM actor",
            available_tables=["actor"]
        )
    )

    # ── Cas 2 : requête valide avec JOIN ───────────────────────────
    print_result(
        question="Show me all movies released this year",
        sql="SELECT film_id, title, release_year FROM film WHERE release_year = YEAR(CURDATE())",
        result=validate(
            sql="SELECT film_id, title, release_year FROM film WHERE release_year = YEAR(CURDATE())",
            available_tables=["film"]
        )
    )

    # ── Cas 3 : tentative d'injection ──────────────────────────────
    print_result(
        question="hack attempt",
        sql="SELECT * FROM actor; DROP TABLE actor",
        result=validate(
            sql="SELECT * FROM actor; DROP TABLE actor",
            available_tables=["actor"]
        )
    )

    # ── Cas 4 : table non autorisée ────────────────────────────────
    print_result(
        question="unauthorized table",
        sql="SELECT * FROM payment",
        result=validate(
            sql="SELECT * FROM payment",
            available_tables=["actor"]   # payment n'est pas dans la liste
        )
    )

    # ── Cas 5 : UPDATE interdit ────────────────────────────────────
    print_result(
        question="write attempt",
        sql="UPDATE actor SET first_name = 'hacked' WHERE actor_id = 1",
        result=validate(
            sql="UPDATE actor SET first_name = 'hacked' WHERE actor_id = 1",
            available_tables=["actor"]
        )
    )