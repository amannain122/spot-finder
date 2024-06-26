
import psycopg2
# import os
# import pandas as pd

# try:
#     from sqlalchemy import create_engine
# except ModuleNotFoundError:

#     from sqlalchemy import create_engine
# try:
#     import psycopg2
# except ModuleNotFoundError:
#     import psycopg2

# print('Libraries imported successfully')


# # create sql engine to connect to redshift

# engine_string = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
#     "awsuser", "Anjitha97", "redshift-cluster-1.cqyedsmaziep.us-east-2.redshift.amazonaws.com", "5439", "dev")
# engine = create_engine(engine_string)

# # redshift-cluster-1.cqyedsmaziep.us-east-2.redshift.amazonaws.com:5439/dev

# print('Engine created successfully')

# print(engine)
# # change the query as needed. <table> should be the database name and the table name.

# sql = """
#     SELECT *
#     FROM <table>
#     LIMIT 5
# """

# print(sql)

# df = pd.read_sql(sql, engine)
# # df


# Connection parameters
dbname = 'your_database_name'
user = 'awswer'
password = 'Anjitha97'
host = "redshift-cluster-1.cqyedsmaziep.us-east-2.redshift.amazonaws.com"
port = '5430'

# Establish connection
conn = psycopg2.connect(dbname=dbname, user=user,
                        password=password, host=host, port=port)

# Create a cursor object using the connection
cur = conn.cursor()

# Example: execute a query
cur.execute("SELECT * FROM api_post;")
rows = cur.fetchall()
print(rows)

# Close cursor and connection
cur.close()
conn.close()
