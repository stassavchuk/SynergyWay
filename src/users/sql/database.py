
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


