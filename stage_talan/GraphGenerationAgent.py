import json
import plotly.graph_objects as go
import plotly.express as px


def generate(executor_result: dict, output_type: str, question: str = "") -> str:
    """
    Génère un graphique Plotly ou un tableau HTML selon output_type.

    Args:
        executor_result : dict retourné par sql_executor.execute()
        output_type     : BAR_CHART / LINE_CHART / PIE_CHART / TABLE / TEXT
        question        : question originale de l'utilisateur (pour le titre)

    Returns:
        HTML string prêt à afficher dans Angular
    """
    rows    = executor_result["rows"]
    columns = executor_result["columns"]

    if not rows:
        return "<p>No data returned.</p>"

    # ── TEXT : valeur unique ───────────────────────────────────────
    if output_type == "TEXT":
        value = list(rows[0].values())[0]
        label = columns[0]
        return f"<div style='font-size:2rem;font-weight:bold;text-align:center'>{label}: {value}</div>"

    # ── TABLE : tableau HTML ───────────────────────────────────────
    if output_type == "TABLE":
        header = "".join(f"<th>{col}</th>" for col in columns)
        body   = ""
        for row in rows:
            cells = "".join(f"<td>{v}</td>" for v in row.values())
            body += f"<tr>{cells}</tr>"
        return f"""
        <table border='1' cellpadding='6' cellspacing='0' style='border-collapse:collapse;width:100%'>
            <thead><tr>{header}</tr></thead>
            <tbody>{body}</tbody>
        </table>"""

    # Pour les graphiques, on a besoin de 2 colonnes minimum
    if len(columns) < 2:
        return "<p>Not enough columns to generate a chart.</p>"

    x_col = columns[0]                          # axe X — catégorie ou date
    y_col = columns[1]                          # axe Y — valeur numérique
    x_vals = [row[x_col] for row in rows]
    y_vals = [row[y_col] for row in rows]

    # ── BAR_CHART ──────────────────────────────────────────────────
    if output_type == "BAR_CHART":
        fig = px.bar(
            x=x_vals, y=y_vals,
            labels={"x": x_col, "y": y_col},
            title=question,
            color=y_vals,
            color_continuous_scale="Blues"
        )

    # ── LINE_CHART ─────────────────────────────────────────────────
    elif output_type == "LINE_CHART":
        fig = px.line(
            x=x_vals, y=y_vals,
            labels={"x": x_col, "y": y_col},
            title=question,
            markers=True
        )

    # ── PIE_CHART ──────────────────────────────────────────────────
    elif output_type == "PIE_CHART":
        fig = px.pie(
            names=x_vals, values=y_vals,
            title=question
        )

    else:
        return "<p>Unknown output type.</p>"

    # Convertir en HTML
    return fig.to_html(full_html=False, include_plotlyjs="cdn")


if __name__ == "__main__":

    # Simule ce que retourne le SQL Executor
    test_cases = [
        {
            "question":   "How many actors?",
            "output_type": "TEXT",
            "executor_result": {
                "status": "success",
                "columns": ["total_actors"],
                "rows": [{"total_actors": 200}],
                "row_count": 1
            }
        },
        {
            "question":   "Number of films per rating",
            "output_type": "BAR_CHART",
            "executor_result": {
                "status": "success",
                "columns": ["rating", "film_count"],
                "rows": [
                    {"rating": "PG",    "film_count": 194},
                    {"rating": "G",     "film_count": 178},
                    {"rating": "NC-17", "film_count": 210},
                    {"rating": "PG-13", "film_count": 223},
                    {"rating": "R",     "film_count": 195},
                ],
                "row_count": 5
            }
        },
        {
            "question":   "Show me all movies released this year",
            "output_type": "TABLE",
            "executor_result": {
                "status": "success",
                "columns": ["film_id", "title", "release_year"],
                "rows": [
                    {"film_id": 1, "title": "ACADEMY DINOSAUR", "release_year": 2006},
                    {"film_id": 2, "title": "ACE GOLDFINGER",   "release_year": 2006},
                ],
                "row_count": 2
            }
        }
    ]

    print("Graph Generation Agent — Test\n")

    for case in test_cases:
        print(f"Q           : {case['question']}")
        print(f"output_type : {case['output_type']}")
        html = generate(case["executor_result"], case["output_type"], case["question"])

        # Sauvegarder dans un fichier HTML pour visualiser
        filename = f"output_{case['output_type'].lower()}.html"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"<html><body>{html}</body></html>")

        print(f"   ✓ Saved → {filename}")
        print()

    print("Open the .html files in your browser to see the charts.")
