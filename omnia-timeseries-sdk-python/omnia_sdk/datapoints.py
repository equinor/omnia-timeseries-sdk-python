"""
Data point resources
"""
import datetime
from typing import Union, List
from ._config import _DATETIME_FORMAT
from ._base import OmniaResource, OmniaResourceList


class DataPoint(OmniaResource):
    """
    An object representing a data point.

    Parameters
    ----------
    time : str, optional
        ISO formatted date time string.
    value : Union[int, float], optional
        Data point value.
    status : int, optional
        Status code.
    """
    def __init__(self, time: str = None, value: Union[int, float] = None, status: int = None):
        self.time = datetime.datetime.strptime(time, _DATETIME_FORMAT)
        self.value = value
        self.status = status


class DataPoints(OmniaResourceList):
    """
    An object representing a list of data points.

    Parameters
    ----------
    time : List[str]
        ISO formatted date time string
    values : List[Union[int, float]]
        Data point values

    """
    def __init__(self, time: List[str], value: List[Union[int, float]]):
        self.resources = [DataPoint(time=t, value=v) for t, v in zip(time, value)]

    @property
    def time(self):
        """List[datetime.datetime]: Datapoint's time."""
        return [r.time for r in self.resources]

    @property
    def value(self):
        """List[Union[int, float]]: Datapoint's value."""
        return [r.value for r in self.resources]