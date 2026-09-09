import os
import json
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect, text

load_dotenv()

DB_URL= f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
def discover_schema():
    engine = create_engine(DB_URL)
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("cnx ok")
    except Exception as e:
        print("cnx failed", e)
        return None

    inspector = inspect(engine)
    schema = {}
   
    inspector = inspect(engine)
    schema = {}
 
    tables = inspector.get_table_names()
    print(f"{len(tables)} tables  : {tables}\n")
 
    for table_name in tables:
 
        # PK 
        pk_columns = inspector.get_pk_constraint(table_name).get("constrained_columns", [])

        # FK
        foreign_keys = [
            {
                "column":            fk["constrained_columns"],
                "references_table":  fk["referred_table"],
                "references_column": fk["referred_columns"],
            }
            for fk in inspector.get_foreign_keys(table_name)
        ]

        # UNIQUE
        unique_constraints = inspector.get_unique_constraints(table_name)
        unique_columns = []

        # CONSTRAINTS
        checks = inspector.get_check_constraints(table_name)

        for uc in unique_constraints:
            unique_columns.extend(uc["column_names"])
 
        # Colonnes
        columns = []
        for col in inspector.get_columns(table_name):
            columns.append({
                "name":        col["name"],
                "type":        str(col["type"]),
                "nullable":    col["nullable"],
                "default":     col["default"],
                "unique": col["name"] in unique_columns,
                "autoincrement": col.get("autoincrement"),
                "check_constraints": checks})
        
        # 5 lignes 
        sample_rows = []
        with engine.connect() as conn:
            result = conn.execute(
                text(f"SELECT * FROM `{table_name}` LIMIT 5")
            )
            sample_rows = [
                dict(row._mapping)
                for row in result
            ]
 
        schema[table_name] = {
            "primary_key":  pk_columns,
            "columns":      columns,
            "foreign_keys": foreign_keys,
            "sample_rows": sample_rows

        }
 
    return schema
 
 
'''def print_schema_summary(schema):
    print("📋 Schéma découvert :\n")
    for table_name, info in schema.items():
        col_names = [c["name"] for c in info["columns"]]
        print(f"  {table_name}({', '.join(col_names)})")
        for fk in info["foreign_keys"]:
            print(f"     ↳ FK: {fk['column']} → {fk['references_table']}.{fk['references_column']}")
    print()'''


if __name__ == "__main__":
    schema = discover_schema()
    # print_schema_summary(schema)

    output_path = os.path.join(os.path.dirname(__file__), "schema_raw.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(schema, f, indent=2, ensure_ascii=False, default=str)
    print(f"Schema saved in : {os.path.abspath(output_path)}")
