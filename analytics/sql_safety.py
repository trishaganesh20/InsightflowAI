import re

FORBIDDEN = [
    "drop", "delete", "update", "insert", "alter", "truncate", "create",
    "grant", "revoke", "replace", "rename", "set", "commit", "rollback"
]

def validate_sql(sql: str) -> tuple[bool, str, str]:
    s = (sql or "").strip().rstrip(";").strip()
    low = s.lower()

    if not low.startswith("select"):
        return False, "Only SELECT statements allowed.", ""

    # block multiple statements
    if ";" in s:
        return False, "Multiple statements not allowed.", ""

    for kw in FORBIDDEN:
        if re.search(r"\b" + re.escape(kw) + r"\b", low):
            return False, f"Forbidden keyword detected: {kw}", ""

    # enforce a safe preview limit
    if re.search(r"\blimit\b", low) is None:
        s = s + " LIMIT 200"

    return True, "OK", s
