from db import sql_select, sql_write


def user_id(email):
    sql_select("SELECT * FROM users WHERE email = %s", [email])