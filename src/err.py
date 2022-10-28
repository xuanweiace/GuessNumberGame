import ER

class MySQLError(Exception):
    """Exception related to operation with MySQL."""




class ProgrammingError():
    """Exception raised for programming errors, e.g. table not found
    or already exists, syntax error in the SQL statement, wrong number
    of parameters specified, etc."""


error_map = {}


def _map_error(exc, *errors):
    for error in errors:
        error_map[error] = exc


_map_error(
    ProgrammingError,
)