from analytics.db import read_sql

def get_schema_context(schema_name: str = "ba_assistant") -> str:
    cols = read_sql(f"""
    SELECT
      table_name AS table_name,
      column_name AS column_name,
      data_type AS data_type,
      is_nullable AS is_nullable,
      column_key AS column_key
    FROM information_schema.columns
    WHERE table_schema = '{schema_name}'
    ORDER BY table_name, ordinal_position;
    """)

    fks = read_sql(f"""
    SELECT
      table_name AS table_name,
      column_name AS column_name,
      referenced_table_name AS referenced_table_name,
      referenced_column_name AS referenced_column_name
    FROM information_schema.key_column_usage
    WHERE table_schema = '{schema_name}'
      AND referenced_table_name IS NOT NULL
    ORDER BY table_name, column_name;
    """)

    # normalize column name casing
    cols.columns = [c.lower() for c in cols.columns]
    fks.columns = [c.lower() for c in fks.columns]

    lines = ["Database schema:"]
    current = None

    for _, r in cols.iterrows():
        t = r["table_name"]
        if t != current:
            lines.append(f"\nTable {t}:")
            current = t

        key = r["column_key"]
        key_txt = " PK" if key == "PRI" else ""
        lines.append(f"  - {r['column_name']} {r['data_type']}{key_txt}")

    if len(fks) > 0:
        lines.append("\nForeign keys:")
        for _, r in fks.iterrows():
            lines.append(
                f"  - {r['table_name']}.{r['column_name']} -> {r['referenced_table_name']}.{r['referenced_column_name']}"
            )

    return "\n".join(lines)
