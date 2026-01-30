import os
from dotenv import load_dotenv
from openai import OpenAI
from analytics.schema_reader import get_schema_context

load_dotenv()  # ✅ loads OPENAI_API_KEY from .env
if not os.environ.get("OPENAI_API_KEY"):
    raise RuntimeError("OPENAI_API_KEY is missing. Add it to .env in the project root and restart Streamlit.")

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

SYSTEM = """You are an expert analytics engineer.
Write MySQL SELECT queries only.
Use only the tables/columns provided in the schema.
Return ONLY SQL. No markdown, no explanations.
"""

def generate_sql(question: str, schema_name: str = "ba_assistant") -> str:
    schema = get_schema_context(schema_name)

    prompt = f"""
Schema:
{schema}

User question:
{question}

Rules:
- MySQL syntax
- SELECT only
- Use explicit JOINs using foreign keys
Return SQL only.
""".strip()

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": prompt},
        ],
        temperature=0,
    )

    return resp.choices[0].message.content.strip().strip("```").strip()
