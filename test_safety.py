from analytics.sql_safety import validate_sql

tests = [
    "SELECT * FROM customers",
    "DELETE FROM customers",
    "SELECT * FROM customers; SELECT * FROM products",
]

for t in tests:
    ok, msg, cleaned = validate_sql(t)
    print("\n---")
    print("IN :", t)
    print("OK :", ok)
    print("MSG:", msg)
    print("OUT:", cleaned)
