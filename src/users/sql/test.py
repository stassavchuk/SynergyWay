import os
import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from contextlib import contextmanager
from random import randint


DEFAULT_DB_NAME = 'postgres'
DB_NAME = 'Users'
USER = 'postgres'
HOST = 'localhost'
PASSWORD = '21041993'


@contextmanager
def cursor(db_name, user, host, password):
    conn = psycopg2.connect(dbname=db_name, user=user, host=host, password=password)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    yield cur

    cur.close()
    conn.commit()
    conn.close()


# OK
def create_database():
    path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(path, 'scripts/create_and_construct_db.sql')

    with open(path, 'r') as f:
        sqltext = f.read()

    with cursor(DEFAULT_DB_NAME, USER, HOST, PASSWORD) as cur:
        cur.execute(sqltext)
        cur.callproc("create_and_construct_db", [DB_NAME])


# OK
def get_all_users():
    with cursor(DB_NAME, USER, HOST, PASSWORD) as cur:
        cur.callproc("all_users", [])
        return cur.fetchall()


# OK
def get_user_data(user_id):
    with cursor(DB_NAME, USER, HOST, PASSWORD) as cur:
        cur.callproc("user_data", [user_id])
        return cur.fetchall()


# OK
def get_user_courses(user_id):
    with cursor(DB_NAME, USER, HOST, PASSWORD) as cur:
        cur.callproc("user_courses", [user_id])
        return cur.fetchall()


# OK
def get_all_courses():
    with cursor(DB_NAME, USER, HOST, PASSWORD) as cur:
        cur.callproc("all_courses", [])
        return cur.fetchall()


# OK
def add_user(name, email, status, phone, m_phone):
    with cursor(DB_NAME, USER, HOST, PASSWORD) as cur:
        cur.callproc("add_user", [name, email, status, phone, m_phone])


# OK
def delete_user(user_id):
    with cursor(DB_NAME, USER, HOST, PASSWORD) as cur:
        cur.callproc("delete_user", [user_id])


# OK
def update_records(user_id, course_list):
    with cursor(DB_NAME, USER, HOST, PASSWORD) as cur:
        cur.callproc("update_records", [user_id, course_list])


def name_generator(n):
    f_name_start = ['Mo', 'He', 'Ja', 'Schmu', 'Schlo']
    f_name_end = ['donei', 'shel', 'mon', 'mo', 'diah']
    l_name_start = ['Gold', 'Wasser', 'Edel', 'Bergen', 'Braun']
    l_name_end = ['berg', 'stein', 'meyer', 'owsky', 'heimer']

    operator = ['050', '067', '095', '063', '093']

    mailbox = ['gmail.com', 'hotmail.com', 'yahoo.com', 'protonmail.com', 'mail.com']

    for i in xrange(n):
        name = str(f_name_start[randint(0, 4)])
        name += str(f_name_end[randint(0, 4)])
        name += ' '
        name += str(l_name_start[randint(0, 4)])
        name += str(l_name_end[randint(0, 4)])

        email = name.replace(' ', '.').lower() + '@' + str(mailbox[randint(0, 4)])

        status = bool(randint(0, 1))

        phone = '+38' + str(operator[randint(0, 4)]) + str(randint(1000000, 9999999))

        m_phone = '+38032' + str(randint(1000000, 9999999))

        yield (name, email, status, phone, m_phone)


def populate_courses():
    with cursor(DB_NAME, USER, HOST, PASSWORD) as cur:
        cur.execute('''
        INSERT INTO courses (course_id, course_name, code) VALUES
          (1,	'Python-Base', 'P012345'),
          (2,	'Python-Database',	'P234567'),
          (3, 'HTML',	'H345678'),
          (4,	'Java-Base',	'J456789'),
          (5,	'JavaScript-Base', 'JS43210');

        ''')


if __name__ == '__main__':
    for i in name_generator(100):
        add_user(*i)

    for i in get_all_users():
        print i
