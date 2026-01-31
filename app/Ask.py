import os, sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
import plotly.express as px

from analytics.db import read_sql
from analytics.sql_generator import generate_sql
from analytics.sql_safety import validate_sql

st.set_page_config(page_title="InsightFlow - Ask", layout="wide")
st.title("Ask InsightFlow 🤖")
st.caption("Type a business question → get SQL → run it safely → see results + chart")

q = st.text_input(
    "Business question",
    placeholder="e.g., Show monthly revenue by region for the last 12 months"
)

if st.button("Generate SQL", type="primary", disabled=not q):
    sql = generate_sql(q)
    st.session_state["sql_raw"] = sql

if "sql_raw" in st.session_state:
    st.subheader("Generated SQL")
    st.code(st.session_state["sql_raw"], language="sql")

    ok, msg, safe_sql = validate_sql(st.session_state["sql_raw"])
    if not ok:
        st.error(msg)
    else:
        st.success("SQL validated")
        st.code(safe_sql, language="sql")

        if st.button("Run Query"):
            df = read_sql(safe_sql)
            st.subheader("Results")
            st.dataframe(df, use_container_width=True)

            # Simple auto-chart: if there's a date-like column and a numeric column
            if len(df.columns) >= 2:
                numeric_cols = df.select_dtypes(include="number").columns.tolist()
                if numeric_cols:
                    y = numeric_cols[0]
                    x = df.columns[0]
                    try:
                        fig = px.line(df, x=x, y=y, title=f"{y} over {x}")
                        st.plotly_chart(fig, use_container_width=True)
                    except Exception:
                        pass
