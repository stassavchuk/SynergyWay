# singleton
class Database:
    """
    Creating database. Reading sql-files and declaration functions of it.
    """

    db_name = 'Users'
    user = 'postgres'
    default_db = 'postgres'
    host = 'localhost'

    def get_db(self):
        pass


class DatabaseConnector:
    def __init__(self):
        self.database = Database.get_db()


# Errors

class DatabaseError(BaseException):
    """Base exception"""
    pass


class DatabaseCreationError(DatabaseError):
    """If something happen during database creation"""
    pass


class DatabaseExecutionError(DatabaseError):
    """If something happen during execution of function"""
    pass


class DatabaseValueError(DatabaseError):
    """Incorrect values input"""
    pass


class DatabaseConnectionError(DatabaseError):
    """If something happen during opening or closing the connection"""
    pass
