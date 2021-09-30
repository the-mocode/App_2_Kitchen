import psycopg2
import os

DB_URL = os.environ.get("DATABASE_URL", "dbname=app2kitchen")

def sql_select(query, parameter):
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute(query, parameter)
    data = cur.fetchall()
    conn.close()
    return data


def sql_write(query, params):
  conn = psycopg2.connect(DB_URL)
  cur = conn.cursor()
  cur.execute(query, params)
  conn.commit()
  conn.close()