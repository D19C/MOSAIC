"""Contains all the functionalities related to Environment Variables"""
# pylint: disable=relative-beyond-top-level
from json import loads
from django.db.utils import ProgrammingError
from ..models.environment_variables import EnvironmentVariables


def getenv(var):
    """ Retrieves requested environment variable. If it doesn"t exists, it will
    return a default value according to its type.

    Parameter
    ---------

    var: string
        Environment var to retrieve

    Return
    ------

    variable: int | float | boolean
        Requested environment variable

    """
    # pylint: disable=no-member
    try:
        variable = EnvironmentVariables.objects.filter(var_name=var).first()
        if not variable:
            return ""
    except ProgrammingError:
        return ""

    try:

        if variable.var_type == "integer":
            return int(variable.var_value)
        if variable.var_type == "float":
            return float(variable.var_value)
        if variable.var_type == "json":
            return loads(variable.var_value)

    except ValueError:
        return 0

    if variable.var_type == "boolean":
        return variable.var_value.lower() == "true"

    return variable.var_value
