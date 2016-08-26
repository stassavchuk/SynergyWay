import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os


class Connector:
    _cursor = None
    _user = None
    _db_name = None
    _password = None
    _host = None
    _db_exist = False

    def __init__(self, user=None, default_db=None, db_name=None, password=None, host=None, test=None):
        user = 'postgres' if not user else user
        default_db = 'postgres' if not default_db else default_db
        test = False if not test else True

        # This should be imported from src.settings
        db_name = 'Users' if not db_name else db_name
        password = '21041993' if not password else password
        host = 'localhost' if not host else host

        if not Connector._db_exist:
            self._create_database(default_db, user, host, password, db_name)
            self._create_cursor(db_name, user, host, password)
            self._create_tables()

            if test:
                # Populate db with test data
                pass

            # Update status of database
            Connector._db_exist = True

        if (user, db_name, password, host) != (Connector._user, Connector._db_name,
                                               Connector._password, Connector._host):
            self._create_cursor(db_name, user, password, host)

    def _create_cursor(self, db_name, user, host, password):
        try:
            conn = psycopg2.connect(dbname=db_name, user=user, host=host, password=password)
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            Connector._cursor = conn.cursor()
            Connector._user, Connector._db_name, Connector._password, Connector._host = user, db_name, password, host
        except psycopg2.Error as e:
            print e.message


    def _create_database(self, default_db, user, host, password, db_name):
        try:
            # Create connection for default database
            conn = psycopg2.connect(dbname=default_db, user=user, host=host, password=password)
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cur = conn.cursor()

            # Creating database
            sql_text = 'CREATE DATABASE "' + db_name + '";'
            cur.execute(sql_text)
        except psycopg2.Error as e:
            print e.message

    def _create_tables(self):
        sql_dir = os.path.dirname(os.path.abspath(__file__))
        sql_path = os.path.join(sql_dir, 'trash/create_tables.sql')
        with open(sql_path, 'r') as f:
            sql_text = f.read()
            try:
                Connector._cursor.execute(sql_text)
            except psycopg2.Error as e:
                print e.message


if __name__ == '__main__':
    c = Connector()
