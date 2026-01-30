import os, sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
from analytics.db import read_sql



import streamlit as st
from analytics.db import read_sql

st.set_page_config(page_title="InsightFlow", layout="wide")

st.title("InsightFlow 🚀")
st.caption("Database Connectivity Check")

try:
    df = read_sql("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'ba_assistant'
        ORDER BY table_name;
    """)

    st.success("Database connected successfully ")
    st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error("Database connection failed ")
    st.exception(e)


counts = read_sql("""
SELECT 'customers' AS table_name, COUNT(*) AS cnt FROM customers
UNION ALL
SELECT 'products', COUNT(*) FROM products;
""")
st.subheader("Row counts")
st.dataframe(counts, use_container_width=True)


more_counts = read_sql("""
SELECT 'orders' AS table_name, COUNT(*) AS cnt FROM orders
UNION ALL SELECT 'order_items', COUNT(*) FROM order_items
UNION ALL SELECT 'subscriptions', COUNT(*) FROM subscriptions
UNION ALL SELECT 'support_tickets', COUNT(*) FROM support_tickets;
""")
st.subheader("More row counts")
st.dataframe(more_counts, use_container_width=True)
