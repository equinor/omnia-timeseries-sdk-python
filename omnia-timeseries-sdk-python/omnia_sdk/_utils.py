"""
Utility functions
"""
import numpy as np
from collections import OrderedDict, defaultdict
from datetime import datetime, timedelta
import uuid
import re
from ._config import _DATETIME_FORMAT


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
            v = v.strftime(_DATETIME_FORMAT)
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