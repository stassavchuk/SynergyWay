"""This module provides class Database that allows to make queries to database.

"""

# from exceptions import DatabaseError
from tools import data_generator, tryexcept
import os
import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from contextlib import contextmanager


__all__ = ['Database']
__version__ = '0.01'
__author__ = 'Stanislav Savchuk'


DEFAULT_DB_NAME = 'postgres'
DB_NAME = 'Users'
USER = 'postgres'
HOST = 'localhost'
PASSWORD = '21041993'


class Database:
    __is_created = False

    def __init__(self):
        self.db_name = DB_NAME
        self.user = USER
        self.host = HOST
        self.password = PASSWORD

        if not Database.__is_created:
            try:
                self.__create_database()
                self.__populate_courses()
                self.__random_populate_db(100)
            except Error:
                pass
            finally:
                Database.__is_created = True

    @contextmanager
    def cursor(self, db_name, user, host, password):
        conn = psycopg2.connect(dbname=db_name, user=user, host=host, password=password)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()

        yield cur

        cur.close()
        conn.commit()
        conn.close()

    def __create_database(self):
        path = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(path, 'scripts/create_and_construct_db.sql')

        with open(path, 'r') as f:
            sqltext = f.read()

        with self.cursor(DEFAULT_DB_NAME, self.user, self.host, self.password) as cur:
            cur.execute(sqltext)
            cur.callproc("create_and_construct_db", [self.db_name])

    def __populate_courses(self):
        with self.cursor(self.db_name, self.user, self.host, self.password) as cur:
            cur.execute('''
            INSERT INTO courses (course_id, course_name, code) VALUES
              (1,	'Python-Base', 'P012345'),
              (2,	'Python-Database',	'P234567'),
              (3, 'HTML',	'H345678'),
              (4,	'Java-Base',	'J456789'),
              (5,	'JavaScript-Base', 'JS43210');

            ''')

    def __random_populate_db(self, n):
        for data in data_generator(n):
            self.add_user(*data)

    # @tryexcept
    def get_all_users(self):
        with self.cursor(self.db_name, self.user, self.host, self.password) as cur:
            cur.callproc("all_users", [])
            return cur.fetchall()

    # @tryexcept
    def get_user_data(self, user_id):
        with self.cursor(self.db_name, self.user, self.host, self.password) as cur:
            cur.callproc("user_data", [user_id])
            return cur.fetchall()

    # @tryexcept
    def get_user_courses(self, user_id):
        with self.cursor(self.db_name, self.user, self.host, self.password) as cur:
            cur.callproc("user_courses", [user_id])
            return cur.fetchall()

    # @tryexcept
    def get_all_courses(self):
        with self.cursor(self.db_name, self.user, self.host, self.password) as cur:
            cur.callproc("all_courses", [])
            return cur.fetchall()

    # @tryexcept
    def add_user(self, name, email, status, phone, m_phone):
        with self.cursor(self.db_name, self.user, self.host, self.password) as cur:
            cur.callproc("add_user", [name, email, status, phone, m_phone])

    # @tryexcept
    def delete_user(self, user_id):
        with self.cursor(self.db_name, self.user, self.host, self.password) as cur:
            cur.callproc("delete_user", [user_id])

    # @tryexcept
    def update_records(self, user_id, course_list):
        with self.cursor(self.db_name, self.user, self.host, self.password) as cur:
            cur.callproc("update_records", [user_id, course_list])


if __name__ == '__main__':
    d = Database()

