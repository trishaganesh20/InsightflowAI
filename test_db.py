from analytics.db import read_sql

df = read_sql("SHOW TABLES;")
print(df)
