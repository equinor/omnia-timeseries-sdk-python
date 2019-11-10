"""
Data moadels of basic OMNIA resources
"""
import json
import datetime
from typing import List, Union
from ._config import _DATETIME_FORMAT
from ._utils import make_serializable


class OmniaResource(object):
    """Basic resource object."""
    def __str__(self):
        return json.dumps(make_serializable(self.dump()), indent=2)

    def __repr__(self):
        return self.__str__()

    def dump(self, camel_case: bool = False):
        """
        Dump the instance into a json serializable Python data type.

        Parameters
        ----------
        camel_case : bool, optional
            Use camelCase for attribute names. Defaults to False.

        Returns
        -------
        Dict[str, Any]
            A dictionary representation of the instance.
        """
        return {key: value for key, value in self.__dict__.items() if value is not None and not key.startswith("_")}


class OmniaResourceList(OmniaResource):
    """List of basic resource objects."""
    resources = list()

    @property
    def count(self):
        """int: Number of resources."""
        return len(self.resources)

    def dump(self, camel_case: bool = False):
        """
        Dump the instance into a json serializable Python data type.

        Parameters
        ----------
        camel_case : bool, optional
            Use camelCase for attribute names. Defaults to False.

        Returns
        -------
        List[Dict[str, Any]]
            A list of dicts representing the instance.
        """
        return [_.dump() for _ in self.resources]


class TimeSeries(OmniaResource):
    """
    Timeseries resource

    Parameters
    ----------
    id : str, optional
        Timeseries indentifier
    external_id : str, optional
        Id from another (external) system
    name : str, optional
        Name of the time series
    description : str, optional
        Description of the time series
    step : bool, optional
        Is it a step time series
    unit : str, optional
        Unit of measure
    created_time : str, optional
        ISO formatted date-time of when the time series was created
    changed_time : str, optional
        ISO formatted date-time of when the time series was last changed
    asset_id : str, optional
        Id of the asset this times eries belong to
    omnia_client : OmniaClient, optional
        OMNIA client.

    """
    def __init__(self, id: str = None, external_id: str = None, name: str = None, description: str = None,
                 step: bool = None, unit: str = None, created_time: str = None, changed_time: str = None,
                 asset_id: str = None, omnia_client = None):
        self.id = id
        self.external_id = external_id
        self.asset_id = asset_id
        self.name = name
        self.description = description
        self.step = step
        self.unit = unit
        self.created_time = datetime.datetime.strptime(created_time, _DATETIME_FORMAT)
        self.changed_time = datetime.datetime.strptime(changed_time, _DATETIME_FORMAT)
        self._omnia_client = omnia_client

    def count(self):
        """int: Number of datapoints in this time series."""
        raise NotImplementedError

    def data(self, start: str = None, end: str = None, limit=None, include_outside_points: bool = False):
        """
        Retrieves datapoints in a given time window according to applied parameters.

        Parameters
        ----------
        id : str
            Time series id
        start: str, optional
            Start of data window, date-time in ISO format (RFC3339), defaults to 1 day ago.
        end: str, optional
            End of data window, date-time in ISO format (RFC3339), defaults to now.
        limit : int, optional
            Limit of datapoints to retrieve from within the time window. Between 1-10 000. The default value is 1000.
        include_outside_points: bool, optional
            Determines whether or not the points immediately prior to and following the time window should be
            included in result.

        Returns
        -------
        DataPoints
            Time series data points in time window.

        Notes
        -----
        ISO date-time format is like "2019-11-07T11:13:21Z".

        """
        return self._omnia_client.time_series.data(self.id, start=start, end=end, limit=limit,
                                                   include_outside_points=include_outside_points)

    def latest(self):
        """DataPoint: Latest data point in time series."""
        raise NotImplementedError

    def first(self):
        """DataPoint: First data point in time series."""
        raise NotImplementedError

    def plot(self, start=None, end=None, aggregates=None, granularity=None, *args, **kwargs):
        """
        PLot time series
        """
        # TODO: pandas
        raise NotImplementedError

    def to_pandas(self):
        raise NotImplementedError


class TimeSeriesList(OmniaResourceList):
    """
    List of TimeSeries

    Parameters
    ----------
    timeseries : List[TimeSeries]
    """
    def __init__(self, timeseries: List[TimeSeries], omnia_client = None):
        self.resources = timeseries
        self._omnia_client = omnia_client

    def plot(self):
        raise NotImplementedError


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

    @property
    def first(self):
        """DataPoint: Data point with the earliest time."""
        return self.resources[0]

    @property
    def last(self):
        """DataPoint: Data point with the latest time."""
        return self.resources[-1]
