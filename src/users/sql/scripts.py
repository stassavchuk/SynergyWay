import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# This should be imported from src.settings
USER = 'stas'
DB = 'postgres'
PASSWORD = '21041993'
HOST = 'localhost'


def create_database(user, default_db, passwd, host):
    conn_text = 'dbname=' + default_db + ' user=' + user + ' host=' + host + ' password=' + passwd

    try:
        conn = psycopg2.connect(conn_text)
    except psycopg2.Error as e:
        print e.message
        return
    except BaseException as e:
        print e.message
        return

    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute("""CREATE DATABASE name;""")


if __name__ == '__main__':
    create_database(USER, DB, PASSWORD, HOST)
