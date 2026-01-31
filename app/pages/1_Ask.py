import os, sys, traceback
import streamlit as st

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, ROOT)

st.set_page_config(page_title="InsightFlow - Ask", layout="wide")

try:
    import plotly.express as px
    from analytics.db import read_sql
    from analytics.sql_generator import generate_sql
    from analytics.sql_safety import validate_sql

    st.title("Ask InsightFlow 🤖")
    st.caption("Ask a business question → get SQL → validate → run → chart")

    question = st.text_input(
        "Business question",
        placeholder="e.g., Show order cancellation rate by region"
    )

    if st.button("Generate SQL", type="primary", disabled=not question):
        st.session_state["sql_raw"] = generate_sql(question)

    if "sql_raw" in st.session_state:
        st.subheader("Generated SQL")
        st.code(st.session_state["sql_raw"], language="sql")

        ok, msg, safe_sql = validate_sql(st.session_state["sql_raw"])
        if not ok:
            st.error(msg)
            st.stop()

        st.success("SQL validated")
        st.code(safe_sql, language="sql")

        if st.button("Run Query"):
            df = read_sql(safe_sql)
            st.subheader("Results")
            st.dataframe(df, use_container_width=True)

            numeric_cols = df.select_dtypes(include="number").columns.tolist()
            if numeric_cols and len(df.columns) >= 2:
                x = df.columns[0]
                y = numeric_cols[0]
                fig = px.bar(df, x=x, y=y, title=f"{y} by {x}")
                st.plotly_chart(fig, use_container_width=True)

except Exception:
    st.error("Ask page crashed. Here is the error:")
    st.code(traceback.format_exc())
