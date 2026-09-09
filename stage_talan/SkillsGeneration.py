import os
import json
import time
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL  = "llama-3.1-8b-instant"

SKILLS_DIR = Path("skills")
SKILLS_DIR.mkdir(exist_ok=True)

#  Prompt

SYSTEM_PROMPT = """You are a database documentation expert for a Text-to-SQL AI system.

Your job is to read a raw database table structure (column names, types, primary keys, foreign keys)
and generate a clear Skills.md file that will help an AI agent understand:
- What this table is about
- What each column means in business terms (even if the name is cryptic like `emp_nbr`, `dt_cre`, `flg_act`)
- How to write correct SQL queries on this table

IMPORTANT RULES:
- If a column name is abbreviated or unclear, infer its meaning from context (table name + other columns + type + sample rows).
- Never invent data that is not in the structure
- Be concise but precise
- Output ONLY the markdown, no explanation, no code block wrapper
- The sample rows are only provided to understand the semantics of the columns.
- Never include real values from the sample rows in the output.
- If the meaning of a column is uncertain, explicitly mention that it is inferred.

OUTPUT FORMAT (follow exactly):
---
name: db_<table_name_lowercase>
description: <one sentence — what this table stores>
---

# Ground Truth: `<TableName>` Table

## 1. Schema & Column Definitions
<For each column: name (type, constraints) — plain English meaning>

## 2. Relationships
<Foreign keys and what they link to. Write "None" if no FK.>

## 3. Query Optimization & Constraints
<3 to 5 tips for writing correct SQL on this table>
"""

FEW_SHOT_EXAMPLES = """
Here are two examples of what you must produce:

─────────────────────────────────────────
EXAMPLE 1

Input:
Table: employees
Primary Key: ['emp_id']
Columns:
- emp_id (INTEGER, PRIMARY KEY, NOT NULL)
- emp_nbr (VARCHAR)
- dt_hire (DATE)
- flg_act (TINYINT)
- dept_id (INTEGER)
Foreign Keys:
- ['dept_id'] → departments.['dept_id']

Output:
---
name: db_employees
description: Stores HR information for all company employees including hiring date and active status.
---

# Ground Truth: `employees` Table

## 1. Schema & Column Definitions
- `emp_id` (INTEGER, PRIMARY KEY): Unique identifier for each employee. Auto-incremented.
- `emp_nbr` (VARCHAR): Employee number — internal HR reference code (e.g. "EMP-00142").
- `dt_hire` (DATE): Hiring date. Use to filter by recruitment period or compute tenure.
- `flg_act` (TINYINT): Active flag — 1 = active, 0 = inactive/terminated. Always filter WHERE flg_act = 1 for current headcount.
- `dept_id` (INTEGER, FK): Department identifier. Join with `departments.dept_id` to get the department name.

## 2. Relationships
- `dept_id` → `departments.dept_id`: Links each employee to their department.

## 3. Query Optimization & Constraints
- Always filter `WHERE flg_act = 1` to exclude terminated staff.
- Use `dt_hire` with DATE functions (MONTH, YEAR) for recruitment period analysis.
- Join `departments` on `dept_id` to retrieve department names in aggregation queries.
- Group by `dept_id` (not `dept_name`) for better index performance.

─────────────────────────────────────────
EXAMPLE 2

Input:
Table: ord_hdr
Primary Key: ['ord_id']
Columns:
- ord_id (INTEGER, PRIMARY KEY, NOT NULL)
- cust_id (INTEGER)
- dt_cre (DATETIME)
- mnt_ttc (DECIMAL)
- sta_ord (VARCHAR)
Foreign Keys:
- ['cust_id'] → customers.['id']

Output:
---
name: db_ord_hdr
description: Order header table — one record per customer order with total amount and status.
---

# Ground Truth: `ord_hdr` Table

## 1. Schema & Column Definitions
- `ord_id` (INTEGER, PRIMARY KEY): Unique order identifier.
- `cust_id` (INTEGER, FK): Customer identifier. Join with `customers.id` for customer details.
- `dt_cre` (DATETIME): Order creation timestamp. Use for time-based sales analysis.
- `mnt_ttc` (DECIMAL): Total order amount including taxes (TTC). Aggregate for revenue reports.
- `sta_ord` (VARCHAR): Order status — 'pending', 'confirmed', 'shipped', 'delivered', 'cancelled'.

## 2. Relationships
- `cust_id` → `customers.id`: Links the order to the customer who placed it.

## 3. Query Optimization & Constraints
- Filter `sta_ord = 'delivered'` when computing realized revenue.
- Use `dt_cre` with MONTH() or DATE_FORMAT() for monthly sales reports.
- Sum `mnt_ttc` grouped by `cust_id` or `dt_cre` for aggregation queries.
- Always join `customers` via `cust_id` to enrich orders with customer names.
─────────────────────────────────────────

Now generate the same for the table below.
"""

def build_prompt(table_name: str, table_info: dict) -> str:
    pk = table_info["primary_key"]

    table_block = f"""Table: {table_name}
Primary Key: {pk}

Columns:
""" + "\n".join(
        f"- {c['name']} ({c['type']})"
        f"{', PRIMARY KEY' if c['name'] in pk else ''}"
        f"{', NOT NULL' if not c['nullable'] else ''}"
        for c in table_info["columns"]
    ) + "\n\nForeign Keys:\n" + (
        "\n".join(
            f"- {fk['column']} → {fk['references_table']}.{fk['references_column']}"
            for fk in table_info["foreign_keys"]
        ) or "None"
    )

    return f"{FEW_SHOT_EXAMPLES}\nInput:\n{table_block}\n\nOutput:"


def generate_all_skills(schema_path: str = "schema_raw.json"):

    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    for table_name, table_info in schema.items():
        print(f"{table_name} ")

        prompt = build_prompt(table_name, table_info)

        response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user",   "content": prompt}
                ],
                temperature=0
            )
        skill_md = response.choices[0].message.content

        output_file = SKILLS_DIR / f"{table_name}.md"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(skill_md)

        print(f"   Skill Saved in {output_file}")

if __name__ == "__main__":
    generate_all_skills("schema_raw.json")