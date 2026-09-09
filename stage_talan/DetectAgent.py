import os
import json
import re
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
SKILLS_DIR = Path("skills")


def load_skills() -> str:
    """Lit tous les fichiers skills/*.md et les concatène."""
    skills_text = ""
    for skill_file in SKILLS_DIR.glob("*.md"):
        skills_text += f"\n\n{'='*40}\n"
        skills_text += f"FILE: {skill_file.name}\n"
        skills_text += f"{'='*40}\n"
        skills_text += skill_file.read_text(encoding="utf-8")
    return skills_text


SYSTEM_PROMPT = """You are a detection agent for a Text-to-SQL system.
Given a user question and a set of database table descriptions (skills),
your job is to detect:
1. The user's intent (what kind of SQL operation is needed)
2. Which tables are relevant to answer the question
3. The best output format to present the results

INTENT types:
- AGGREGATION: COUNT, SUM, AVG, GROUP BY queries
- FILTER: SELECT with WHERE conditions
- LOOKUP: simple SELECT to retrieve records
- JOIN: query involving multiple tables
- SORT: ORDER BY queries
- COMPARISON: comparing values across groups

OUTPUT_TYPE based on the data expected:
- BAR_CHART: comparisons between categories (e.g. count per department)
- LINE_CHART: trends over time (e.g. sales per month)
- PIE_CHART: proportions (e.g. percentage per category, max 6 categories)
- TABLE: detailed records, many columns, or when user says "list" or "show"
- TEXT: single value result (e.g. total count, average)

RULES:
- Output ONLY a valid JSON object, nothing else
- No explanation, no markdown, no code block
- tables must be a list of table names exactly as they appear in the skills

OUTPUT FORMAT:
{
  "intent": "<INTENT>",
  "tables": ["<table1>", "<table2>"],
  "output_type": "<OUTPUT_TYPE>",
  "reason": "<one sentence explaining why>"
}
"""

EXAMPLES = """
EXAMPLE 1:
Question: "How many employees per department?"
Output:
{"intent": "AGGREGATION", "tables": ["employees", "departments"], "output_type": "BAR_CHART", "reason": "Counting employees grouped by department — bar chart fits category comparison."}

EXAMPLE 2:
Question: "Show me all students enrolled this month"
Output:
{"intent": "FILTER", "tables": ["students", "enrollments"], "output_type": "TABLE", "reason": "User wants a list of records filtered by date — table format fits."}

EXAMPLE 3:
Question: "What is the average salary?"
Output:
{"intent": "AGGREGATION", "tables": ["employees"], "output_type": "TEXT", "reason": "Single aggregated value — no chart needed."}

EXAMPLE 4:
Question: "Show revenue evolution by month this year"
Output:
{"intent": "AGGREGATION", "tables": ["orders"], "output_type": "LINE_CHART", "reason": "Revenue over time — line chart fits temporal trends."}

Now answer for the question below.
"""


def detect(user_question: str, session_history: list = []) -> dict:
    """
    Analyse la question utilisateur.
    Retourne : intent + tables + output_type + reason
    """
    skills_context = load_skills()

    # Mémoire conversationnelle — max 3 derniers échanges
    session_context = ""
    if session_history:
        session_context = "\n\nPREVIOUS CONVERSATION:\n"
        for msg in session_history[-3:]:
            session_context += f"User: {msg['question']}\n"
            session_context += f"Tables used: {msg['tables']}\n"

    user_prompt = (
        EXAMPLES
        + f"\n\nAVAILABLE DATABASE SKILLS:\n{skills_context}"
        + session_context
        + f"\n\nQuestion: {user_question}\n\nOutput:"
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

    # Parser le JSON — si le LLM ajoute du texte autour on l'extrait
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

    test_questions = [
        "How many actors ?",
        
        "Show me all movies released this year",
    ]

    print("Detection Agent — Test\n")

    for question in test_questions:
        print(f"Q: {question}")
        result = detect(question)
        print(f"   intent      : {result['intent']}")
        print(f"   tables      : {result['tables']}")
        print(f"   output_type : {result['output_type']}")
        print(f"   reason      : {result['reason']}")
        print()