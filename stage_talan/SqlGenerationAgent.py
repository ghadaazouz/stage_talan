import os
import json
import re
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
SKILLS_DIR = Path("skills")


def load_relevant_skills(tables: list) -> str:
    """Charge uniquement les skills des tables détectées."""
    skills_text = ""
    for table in tables:
        skill_file = SKILLS_DIR / f"{table}.md"
        if skill_file.exists():
            skills_text += f"\n\n{'='*40}\n"
            skills_text += f"TABLE: {table}\n"
            skills_text += f"{'='*40}\n"
            skills_text += skill_file.read_text(encoding="utf-8")
        else:
            print(f"   ⚠️  No skill file found for: {table}")
    return skills_text


SYSTEM_PROMPT = """You are a SQL generation expert for a Text-to-SQL system.
Given a user question, the detected intent, and the relevant table schemas (skills),
generate a correct and optimized MySQL SELECT query.

RULES:
- Generate ONLY a SELECT query — never INSERT, UPDATE, DELETE, DROP
- Use exact table and column names as defined in the skills
- Always use table aliases for readability
- Add WHERE, GROUP BY, ORDER BY clauses based on the intent
- Output ONLY a valid JSON object, nothing else

OUTPUT FORMAT:
{
  "sql": "<the SQL query>",
  "explanation": "<one sentence explaining what the query does>"
}
"""

EXAMPLES = """
EXAMPLE 1:
Question: "How many employees per department?"
Intent: AGGREGATION
Tables: employees, departments
Skills:
- employees: emp_id (PK), name, dept_id (FK→departments), hire_date
- departments: dept_id (PK), dept_name

Output:
{"sql": "SELECT d.dept_name, COUNT(e.emp_id) AS employee_count FROM employees e JOIN departments d ON e.dept_id = d.dept_id GROUP BY d.dept_id, d.dept_name ORDER BY employee_count DESC", "explanation": "Counts employees per department by joining both tables and grouping by department."}

EXAMPLE 2:
Question: "How many orders?"
Intent: AGGREGATION
Tables: orders
Skills:
- orders: order_id (PK), customer_id, order_date, total_amount, status

Output:
{"sql": "SELECT COUNT(order_id) AS total_orders FROM orders", "explanation": "Counts the total number of orders in the table."}

EXAMPLE 3:
Question: "Show me all students enrolled this month"
Intent: FILTER
Tables: students, enrollments
Skills:
- students: student_id (PK), first_name, last_name, email
- enrollments: enrollment_id (PK), student_id (FK), enrollment_date

Output:
{"sql": "SELECT s.first_name, s.last_name, s.email, e.enrollment_date FROM students s JOIN enrollments e ON s.student_id = e.student_id WHERE MONTH(e.enrollment_date) = MONTH(CURDATE()) AND YEAR(e.enrollment_date) = YEAR(CURDATE()) ORDER BY e.enrollment_date DESC", "explanation": "Retrieves students enrolled in the current month."}

Now generate for the question below.
"""


def generate_sql(user_question: str, detection_result: dict, feedback: str = None) -> dict:
    """
    Génère une requête SQL à partir de la question et du résultat du Detection Agent.

    Args:
        user_question    : question utilisateur
        detection_result : dict retourné par detection_agent.detect()

    Returns:
        dict avec sql + explanation
    """
    intent = detection_result["intent"]
    tables = detection_result["tables"]

    skills_context = load_relevant_skills(tables)

    feedback_block = ""
    if feedback:
        feedback_block = f"\n\nPREVIOUS ATTEMPT REJECTED:\n{feedback}\nFix the SQL."

    user_prompt = (
        EXAMPLES
        + f"\n\nQuestion: {user_question}"
        + f"\nIntent: {intent}"
        + f"\nTables: {', '.join(tables)}"
        + f"\nSkills:\n{skills_context}"
        + feedback_block 
        + "\n\nOutput:"
    )

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": user_prompt}
        ],
        temperature=0
    )

    raw = response.choices[0].message.content.strip()

    try:
        result = json.loads(raw)
    except json.JSONDecodeError:
        match = re.search(r'\{.*\}', raw, re.DOTALL)
        if match:
            result = json.loads(match.group())
        else:
            raise ValueError(f"Invalid JSON returned:\n{raw}")

    return result


if __name__ == "__main__":

    # Résultats réels du Detection Agent
    test_cases = [
        {
            "question": "How many actors ?",
            "detection": {
                "intent": "AGGREGATION",
                "tables": ["actor"],
                "output_type": "TEXT",
                "reason": "Single aggregated value — no chart needed."
            }
        },
        {
            "question": "Show me all movies released this year",
            "detection": {
                "intent": "FILTER",
                "tables": ["film"],
                "output_type": "TABLE",
                "reason": "User wants a list of records filtered by release year."
            }
        }
    ]

    print("SQL Generation Agent — Test\n")

    for case in test_cases:
        print(f"Q: {case['question']}")
        result = generate_sql(case["question"], case["detection"])
        print(f"   SQL         : {result['sql']}")
        print(f"   Explanation : {result['explanation']}")
        print()