import os
from dotenv import load_dotenv
import mysql.connector
import pandas as pd

load_dotenv()

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
    )

def run_query(query):
    conn = get_connection()
    try:
        df = pd.read_sql(query, conn)
        return df
    finally:
        conn.close()

import os
from dotenv import load_dotenv
import mysql.connector
import pandas as pd

load_dotenv()

def get_conn():
    return mysql.connector.connect(
        host=os.environ["DB_HOST"],
        port=int(os.environ.get("DB_PORT", "3306")),
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DB_NAME"],
    )

def read_sql(query: str) -> pd.DataFrame:
    conn = get_conn()
    try:
        df = pd.read_sql(query, conn)
        return df
    finally:
        conn.close()
