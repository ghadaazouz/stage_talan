from DetectAgent import detect
from SqlGenerationAgent import generate_sql
from SqlValidator import validate
from SqlExecutor import execute
from GraphGenerationAgent import generate

MAX_RETRIES = 2


def run(user_question: str, session_history: list = []) -> dict:
    """
    Pipeline complet :
    question → detection → SQL → validation (retry x2) → execution → visualisation
    """

    print(f"\n{'='*55}")
    print(f"Q: {user_question}")
    print(f"{'='*55}")

    # ── Étape 1 : Detection Agent ──────────────────────────────────
    print("\n[1] Detection Agent...")
    detection = detect(user_question, session_history)
    print(f"    intent      : {detection['intent']}")
    print(f"    tables      : {detection['tables']}")
    print(f"    output_type : {detection['output_type']}")

    # ── Étape 2 + 3 : SQL Generation + Validation avec retry ───────
    feedback   = None
    validation = None
    sql_result = None

    for attempt in range(1, MAX_RETRIES + 1):

        print(f"\n[2] SQL Generation Agent (attempt {attempt}/{MAX_RETRIES})...")
        sql_result = generate_sql(user_question, detection, feedback=feedback)
        print(f"    sql         : {sql_result['sql']}")
        print(f"    explanation : {sql_result['explanation']}")

        print(f"\n[3] SQL Validator...")
        validation = validate(sql_result["sql"], detection["tables"])
        print(f"    status      : {validation['status']}")
        print(f"    risk_level  : {validation['risk_level']}")

        if validation["status"] == "VALIDATED":
            print(f"    ✓ SQL validated")
            break

        # Rejeté → feedback pour le prochain essai
        print(f"    ✗ REJECTED : {validation['errors']}")
        feedback = f"Previous attempt rejected: {validation['errors']}. Fix the SQL."

        if attempt == MAX_RETRIES:
            print(f"\n✗ Max retries reached — pipeline stopped.")
            return {
                "status":      "FAILED",
                "errors":      validation["errors"],
                "output_type": detection["output_type"],
                "html":        "<p>Could not generate a valid SQL query.</p>"
            }

    # ── Étape 4 : SQL Executor ─────────────────────────────────────
    print(f"\n[4] SQL Executor...")
    exec_result = execute(validation["sql_clean"])
    print(f"    status      : {exec_result['status']}")
    print(f"    row_count   : {exec_result['row_count']}")
    print(f"    columns     : {exec_result['columns']}")

    if exec_result["status"] == "error":
        return {
            "status":      "ERROR",
            "errors":      [exec_result["error"]],
            "output_type": detection["output_type"],
            "html":        f"<p>Execution error: {exec_result['error']}</p>"
        }

    # ── Étape 5 : Graph Generation Agent ──────────────────────────
    print(f"\n[5] Graph Generation Agent...")
    html = generate(exec_result, detection["output_type"], user_question)
    print(f"    output_type : {detection['output_type']}")
    print(f"    ✓ Output generated")

    # Sauvegarder dans un fichier HTML
    output_file = f"result.html"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"""
        <html>
        <head><title>AskUrDB — Result</title></head>
        <body style="font-family:sans-serif;padding:2rem">
            <h2>{user_question}</h2>
            <p><b>SQL:</b> <code>{validation['sql_clean']}</code></p>
            <p><i>{sql_result['explanation']}</i></p>
            <hr>
            {html}
        </body>
        </html>
        """)
    print(f"\n✓ Result saved → {output_file}")
    print(f"  Open result.html in your browser to see the output.")

    # Mettre à jour la session memory
    session_history.append({
        "question": user_question,
        "tables":   detection["tables"],
        "sql":      validation["sql_clean"]
    })

    return {
        "status":      "SUCCESS",
        "sql":         validation["sql_clean"],
        "explanation": sql_result["explanation"],
        "output_type": detection["output_type"],
        "row_count":   exec_result["row_count"],
        "html":        html
    }


if __name__ == "__main__":

    session = []   # mémoire conversationnelle partagée entre les questions

    questions = [
        "How many actors?",
        "Show me all movies released this year",
    ]

    for question in questions:
        result = run(question, session)
        print(f"\n→ STATUS : {result['status']}")
        if result["status"] == "SUCCESS":
            print(f"   rows    : {result['row_count']}")
            print(f"   output  : {result['output_type']}")