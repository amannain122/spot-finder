
import redshift_connector
import psycopg2
# # import os
# # import pandas as pd

# # try:
# #     from sqlalchemy import create_engine
# # except ModuleNotFoundError:

# #     from sqlalchemy import create_engine
# # try:
# #     import psycopg2
# # except ModuleNotFoundError:
# #     import psycopg2

# # print('Libraries imported successfully')


# # # create sql engine to connect to redshift

# # engine_string = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
# #     "awsuser", "Anjitha97", "redshift-cluster-1.cqyedsmaziep.us-east-2.redshift.amazonaws.com", "5439", "dev")
# # engine = create_engine(engine_string)

# # # redshift-cluster-1.cqyedsmaziep.us-east-2.redshift.amazonaws.com:5439/dev

# # print('Engine created successfully')

# # print(engine)
# # # change the query as needed. <table> should be the database name and the table name.

# # sql = """
# #     SELECT *
# #     FROM <table>
# #     LIMIT 5
# # """

# # print(sql)

# # df = pd.read_sql(sql, engine)
# # # df


# Connection parameters
dbname = 'dev'
user = 'awswer'
password = 'Anjitha97'
host = "redshift-cluster-1.cqyedsmaziep.us-east-2.redshift.amazonaws.com"
port = '5439'

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


# Connects to Redshift cluster using AWS credentials
conn = redshift_connector.connect(
    host='redshift-cluster-1.cqyedsmaziep.us-east-2.redshift.amazonaws.com',
    database='dev',
    user='awsuser',
    password='Anjitha97'
)

cursor: redshift_connector.Cursor = conn.cursor()
cursor.execute("create Temp table parking(locationName varchar,space varchar)")
cursor.executemany("insert into parking (locationName, space) values (%s, %s)",
                   [
                       ('Bloor Younge', '10'),
                       ('4000 victoria park', '20')
                   ]
                   )
cursor.execute("select * from parking")

result: tuple = cursor.fetchall()
print(result)
