import psycopg2


def sql_select(query, parameter):
    conn = psycopg2.connect("dbname=app2kitchen")
    cur = conn.cursor()
    cur.execute(query, parameter)
    data = cur.fetchall()
    conn.close()
    return data


def sql_write(query, params):
  conn = psycopg2.connect("dbname=app2kitchen")
  cur = conn.cursor()
  cur.execute(query, params)
  conn.commit()
  conn.close()