"""
Utility functions
"""
import numpy as np
from collections import OrderedDict, defaultdict
from datetime import datetime, timedelta
import uuid
import re
from ._config import Config

# compile regex for camel case to snake case
first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')


def make_serializable(d):
    """
    Convert data types within dict/list to JSON serializable.

    Parameters
    ----------
    d : dict or list

    Returns
    -------
    dict or list
        Data structure of same type as input.

    Notes
    -----
    numpy.ndarray is converted to list.
    datetime.datetime object is converted to ISO format string
    datetime.timedelta object is converted to float (total seconds).
    UUID is converted to string.
    """

    def convert_dict(dd):
        for k, v in dd.items():
            if type(v) in (dict, OrderedDict, defaultdict):
                dd[k] = convert_dict(v)
            else:
                dd[k] = convert_value(v, key=k)
        return dd

    def convert_value(v, key=""):
        if isinstance(v, list):
            v = [convert_value(_) for _ in v]
        elif isinstance(v, uuid.UUID):
            v = str(v)
        elif isinstance(v, np.ndarray):
            if v.ndim > 1:
                raise NotImplementedError(f"Unable to JSON serialize multidimensional ndarrays. Key = '{key}'.")
            v = list(v)
        elif isinstance(v, datetime):
            v = v.isoformat()
        elif isinstance(v, timedelta):
            v = v.total_seconds()
        elif type(v) in (dict, OrderedDict, defaultdict):
            v = convert_dict(v)
        return v

    # convert numpy arrays to lists (only 1-dim arrays are handled)
    # why? because json.dump will raise TypeError if any of the submitted data is a numpy ndarray
    if type(d) in (dict, OrderedDict, defaultdict):
        d = convert_dict(d)
    elif isinstance(d, list):
        d = [convert_value(v) for v in d]
    else:
        raise NotImplementedError(f"Unable to convert object of type '{type(d)}' to JSON serializable.")
    return d


def to_snake_case(d):
    """
    Convert data with camelCase keys to snake_case

    Parameters
    ----------
    d : str or list or dict
        Data with camelCase keys

    Returns
    -------
    str or list or dict
        Data with snake case keys
    """
    def snake(s):
        s1 = first_cap_re.sub(r'\1_\2', s)
        return all_cap_re.sub(r'\1_\2', s1).lower()

    if isinstance(d, str):
        return snake(d)
    elif isinstance(d, list):
        return [to_snake_case(_) for _ in d]
    elif isinstance(d, dict):
        dd = dict()
        for k, v in d.items():
            if isinstance(k, str):
                k = snake(k)

            if isinstance(v, (list, dict)):
                v = to_snake_case(v)

            dd[k] = v
        return dd


def to_camel_case(d):
    """
    Convert data with snake_case keys to lowerCamelCase

    Parameters
    ----------
    d : str or list or dict
        Data with snake case keys

    Returns
    -------
    str or list or dict
        Data with camel case keys
    """
    def camel(s):
        first, *others = s.split('_')
        return ''.join([first.lower(), *map(str.title, others)])

    if isinstance(d, str):
        return camel(d)
    elif isinstance(d, list):
        return [to_camel_case(_) for _ in d]
    elif isinstance(d, dict):
        dd = dict()
        for k, v in d.items():
            if isinstance(k, str):
                k = camel(k)

            if isinstance(v, (list, dict)):
                v = to_camel_case(v)

            dd[k] = v
        return dd


def to_omnia_datetime_string(d):
    """
    Convert date time object to formatted date time string.

    Parameters
    ----------
    d : datetime
        Date time object

    Returns
    -------
    str
        Formatted date time string.
    """
    assert isinstance(d, datetime)

    return d.strftime(Config.datetime_format)


def from_datetime_string(s):
    """
    Convert formatted date time string to date time object.

    Parameters
    ----------
    s : str
        ISO RFC3339 formatted date time string

    Returns
    -------
    datetime
        Date time object.

    Notes
    -----
    Examples of  ISO RFC 3339 formatted date time strings
        2008-09-03T20:56:35.450686Z
        2008-09-03T20:56:35.450686+00:00
        2008-09-03T20:56:35.450686+05:00
        2008-09-03T20:56:35.450686-10:30

    """
    # datetime.fromisoformat() does not support Z as short notation for Zulu-time aka. +00:00
    s = s.replace("Z", "+00:00")

    # datetime.fromisoformat() and .strptime() does only handle 0, 3 or 6 decimal places (microseconds) but I frequently
    # encounter deviations like 7 decimals. Truncate datetime string to 26 characters (6 decimals).
    dt, tz = s.split("+")
    s = "+".join([dt[:26], tz])

    return datetime.fromisoformat(s)
