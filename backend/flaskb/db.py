"""
Database access layer. We use tradition SQL connectors/drivers that
implement Python's own DB-API 2.0.

(c) Joao Galamba, 2022
$LICENSE(MIT)
"""

from contextlib import contextmanager
from getpass import getpass
from typing import NewType, Optional
from mysql.connector import connect, Error, pooling


DBObject = NewType('DBOjbect', dict)

############################################################################
##
##      DB INITIALIZATION
##
############################################################################

_CONN_POOL: pooling.MySQLConnectionPool = None

def init_db_connector(**db_config):
    global _CONN_POOL        # pylint: disable=global-statement
    _CONN_POOL = pooling.MySQLConnectionPool(
        pool_name = 'webquiz_pool', 
        pool_size = 3,
        **db_config
    )
#:

############################################################################
##
##      DB API
##
############################################################################

def authenticate_user(
        username: str, 
        password: str, 
        case_converter=lambda col: col
) -> Optional[DBObject]:
    with cursor_from_pool(_CONN_POOL) as cursor:
        cursor.callproc('AuthenticateUser', [username, password])
        users_result_set = next(cursor.stored_results()) 
        assert 0 <= users_result_set.rowcount <= 1
        if users_result_set.rowcount:
            user_row_values = next(users_result_set)
            user_col_names = (
                case_converter(col_name) 
                for col_name in users_result_set.column_names
            )
            return DBObject(dict(zip(user_col_names, user_row_values)))
        #:
    #:
    return None
#:

def get_user_info(
        user_id: int, 
        case_converter=lambda col: col
) -> Optional[DBObject]:
    with cursor_from_pool(_CONN_POOL) as cursor:
        cursor.callproc('GetUserInfo', [user_id])
        users_result_set = next(cursor.stored_results()) 
        assert 0 <= users_result_set.rowcount <= 1
        if users_result_set.rowcount:
            user_row_values = next(users_result_set)
            user_col_names = (
                case_converter(col_name) 
                for col_name in users_result_set.column_names
            )
            return DBObject(dict(zip(user_col_names, user_row_values)))
        #:
    #:
    return None
#:

############################################################################
##
##      DB UTILS
##
############################################################################

@contextmanager
def cursor_from_pool(pool: pooling.MySQLConnectionPool):
    with pool.get_connection() as connection:
        with connection.cursor() as cursor:
            yield cursor   # cursor will be closed by the inner with
#:

def try_connection():
    """
    Just for interactive testing purposes.
    """
    try:
        with connect(
                host="192.168.56.104",
                user=input("Enter username: "),
                password=getpass("Enter password: "),
        ) as connection:
            print(connection)
    except Error as e:
        print(e)
#:

