"""Creating database and tables"""


import psycopg2
from psycopg2 import Error as Err
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os

# Create cursor for default database
conn = psycopg2.connect(dbname='postgres', user='postgres', host='localhost', password='21041993')
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur = conn.cursor()

# Create database with default database 'postgres'
try:
    cur.execute("""CREATE DATABASE "Users1";""")
except Err as e:
    print 'Fail: ', e.message

# Create cursor for custom database
conn = psycopg2.connect(dbname='Users', user='postgres', host='localhost', password='21041993')
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur = conn.cursor()

# Create tables of custom database
sql_dir = os.path.dirname(os.path.abspath(__file__))
sql_path = os.path.join(sql_dir, 'create_tables.sql')

with open(sql_path, 'r') as f:
    sql_text = f.read()

try:
    cur.execute(sql_text)
except Err as e:
    print 'Fail: ', e.message


# Fill tables with test data
sql_path = os.path.join(sql_dir, 'test_data.sql')

with open(sql_path, 'r') as f:
    sql_text = f.read()

try:
    cur.execute(sql_text)
except Err as e:
    print 'Fail: ', e.message
