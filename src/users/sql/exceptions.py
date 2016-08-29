"""This module provides exceptions of Database.

"""

__all__ = ['DatabaseError']
__version__ = '0.01'
__author__ = 'Stanislav Savchuk'


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
