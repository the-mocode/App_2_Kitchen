from db import sql_select, sql_write


def user_id(email):
   result = sql_select("SELECT * FROM users WHERE email = %s", [email])
   return result