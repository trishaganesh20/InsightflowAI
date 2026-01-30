import streamlit as st

st.set_page_config(page_title="InsightFlow", layout="wide")
st.title("InsightFlow 🚀")
st.write("If you can see this, Streamlit is working ✅")

import streamlit as st
from analytics.db import run_query

st.title("InsightFlow 🚀")
st.write("Testing database connection...")

try:
    df = run_query("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'ba_assistant';
    """)

    st.success("Database connected successfully ✅")
    st.dataframe(df)

except Exception as e:
    st.error("Database connection failed ❌")
    st.write(e)
