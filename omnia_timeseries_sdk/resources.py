"""
Data models of basic OMNIA resources
"""
import json
import pandas as pd
import matplotlib.pyplot as plt
from typing import List, Union
from ._utils import make_serializable, from_datetime_string, to_camel_case


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
        d = {key: value for key, value in self.__dict__.items() if value is not None and not key.startswith("_")}
        if camel_case:
            d = {to_camel_case(key): value for key, value in d.items()}

        return d

    def to_pandas(self, ignore: List[str] = None):
        """
        Convert the instance into a pandas DataFrame.

        Parameters
        ----------
        ignore : List[str]
            List of row keys to not include when converting to a data frame.

        Returns
        -------
        pandas.DataFrame
            The dataframe.
        """
        ignore = list() if ignore is None else ignore
        dumped = self.dump()

        df = pd.DataFrame(columns=["value"])
        for name, value in dumped.items():
            if name not in ignore:
                df.loc[name] = [value]
        return df


class OmniaResourceList(OmniaResource):
    """List of basic resource objects."""
    resources = list()

    def __iter__(self):
        for r in self.resources:
            yield r

    def __len__(self):
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
        return [_.dump(camel_case=camel_case) for _ in self]

    def to_pandas(self, ignore: List[str] = None):
        """
        Convert the instance into a pandas DataFrame.

        Returns
        -------
        pandas.DataFrame
            The dataframe.
        """
        return pd.DataFrame(self.dump())


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
        self.created_time = from_datetime_string(created_time)
        self.changed_time = from_datetime_string(changed_time)
        self._omnia_client = omnia_client

    def count(self):
        """int: Number of datapoints in this time series."""
        raise NotImplementedError

    def data(self, start: str = None, end: str = None, limit=None, include_outside_points: bool = False):
        """
        Retrieves datapoints in a given time window according to applied parameters.

        Parameters
        ----------
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
        # TODO: Collect aggregated data (specify aggregates and granularity)
        return self._omnia_client.time_series.data(self.id, start=start, end=end, limit=limit,
                                                   include_outside_points=include_outside_points)

    def first(self, after: str = None):
        """
        Retrieves the first data point of the time series.

        Parameters
        ----------
        after : str, optional
            ISO formatted date-time string. Only look for data points after this time.

        Returns
        -------
        DataPoint
            The data point.
        """
        return self._omnia_client.time_series.first_data(self.id, after_time=after)

    def latest(self, before: str = None):
        """
        Retrieves the last data point of the time series.

        Parameters
        ----------
        before : str, optional
            ISO formatted date-time string. Only look for data points before this time.

        Returns
        -------
        DataPoint
            The data point.
        """
        return self._omnia_client.time_series.latest_data(self.id, before_time=before)

    def plot(self, start: str = None, end: str = None, limit=None, include_outside_points: bool = False, **kwargs):
        """
        Plot data points in a given time window.

        Parameters
        ----------
        start: str, optional
            Start of data window, date-time in ISO format (RFC3339), defaults to 1 day ago.
        end: str, optional
            End of data window, date-time in ISO format (RFC3339), defaults to now.
        limit : int, optional
            Limit of datapoints to retrieve from within the time window. Between 1-10 000. The default value is 1000.
        include_outside_points: bool, optional
            Determines whether or not the points immediately prior to and following the time window should be
            included in result.
        kwargs
            See pandas.DataFrame.plot for options.
        """
        # TODO: Collect aggregated data (specify aggregates and granularity)
        dps = self.data(start=start, end=end, limit=limit, include_outside_points=include_outside_points)
        dps.plot(**kwargs)


class TimeSeriesList(OmniaResourceList):
    """
    List of TimeSeries

    Parameters
    ----------
    timeseries : List[TimeSeries]
        The various time series.
    """
    def __init__(self, timeseries: List[TimeSeries], omnia_client=None):
        self.resources = timeseries
        self._omnia_client = omnia_client

    def data(self, start: str = None, end: str = None, limit=None, include_outside_points: bool = False):
        """
        Retrieves datapoints in a given time window according to applied parameters.

        Parameters
        ----------
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
        DataPointsList
            List of data points in time window for the various time series.

        """
        dps = [ts.data(start=start, end=end, limit=limit, include_outside_points=include_outside_points) for ts in self]
        return DataPointsList(dps)

    def plot(self, start: str = None, end: str = None, limit=None, include_outside_points: bool = False, **kwargs):
        """
        Plot data points from various time series in a given time window.

        Parameters
        ----------
        start: str, optional
            Start of data window, date-time in ISO format (RFC3339), defaults to 1 day ago.
        end: str, optional
            End of data window, date-time in ISO format (RFC3339), defaults to now.
        limit : int, optional
            Limit of datapoints to retrieve from within the time window. Between 1-10 000. The default value is 1000.
        include_outside_points: bool, optional
            Determines whether or not the points immediately prior to and following the time window should be
            included in result.
        kwargs
            See pandas.DataFrame.plot for options.
        """
        dps = self.data(start=start, end=end, limit=limit, include_outside_points=include_outside_points)
        dps.plot(**kwargs)


class DataPoint(OmniaResource):
    """
    An object representing a data point.

    Parameters
    ----------
    id : str, optional
        Id of the time series which the datapoints belong to.
    name : str, optional
        Name of the time series which the datapoints belong to.
    unit : str, optional
        Physical unit of measure.
    time : str, optional
        ISO formatted date time string.
    value : Union[int, float], optional
        Data point value.
    status : int, optional
        Status code.
    """

    # TODO: Create aggregate properties (max, min, stdev, count etc), defined on init if any
    def __init__(self, id: str = None, name: str = None, unit: str = None, time: str = None,
                 value: Union[int, float] = None, status: int = None):
        self.id = id
        self.name = name
        self.unit = unit
        self.time = from_datetime_string(time)
        self.value = value
        self.status = status


class DataPoints(OmniaResourceList):
    """
    An object representing a list of data points.

    Parameters
    ----------
    id : str, optional
        Id of the time series which the datapoints belong to.
    name : str, optional
        Name of the time series which the datapoints belong to.
    unit : str, optional
        Physical unit of measure.
    time : List[str], optional
        ISO formatted date time string
    values : List[Union[int, float]], optional
        Data point values

    """
    # TODO: Create aggregate properties (max, min, stdev, count etc), based on DataPoint
    def __init__(self, id: str = None, name: str = None, unit: str = None, time: List[str] = None,
                 value: List[Union[int, float]] = None):
        self.resources = [DataPoint(time=t, value=v) for t, v in zip(time, value)]
        self.id = id
        self.name = name
        self.unit = unit

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
        dumped = {
            "id": self.id,
            "name": self.name,
            "unit": self.unit,
            "datapoints": [_.dump(camel_case=camel_case) for _ in self]
        }
        return dumped

    def plot(self, **kwargs):
        """
        Plot data points.

        Parameters
        ----------
        kwargs
            See pandas.DataFrame.plot for options.
        """
        self.to_pandas().plot(**kwargs)
        plt.show()

    def to_pandas(self, column_name: str = "name"):
        """
        Convert the data points into a pandas DataFrame.

        Parameters
        ----------
        column_name: {name, id}
            Which field to use as column header. Defaults to 'name'.

        Returns
        -------
        pandas.DataFrame
            The dataframe

        """
        # TODO: Add aggregates when ready
        if column_name == "name":
            header = f"{self.name} [{self.unit}]"
        else:
            header = f"{self.id} [{self.unit}]"

        data = {
            header: self.value
        }

        df = pd.DataFrame(data, index=pd.DatetimeIndex(data=self.time))
        return df


class DataPointsList(OmniaResourceList):
    """
    An object representing a list of data points for different time series.

    Parameters
    ----------
    dps : List[DataPoints]
        Data points
    """
    def __init__(self, dps: List[DataPoints]):
        self.resources = dps

    def plot(self, **kwargs):
        """
        Plot data points.

        Parameters
        ----------
        kwargs
            See pandas.DataFrame.plot for options
        """
        self.to_pandas().plot(**kwargs)
        plt.show()

    def to_pandas(self, column_names: str = "name"):
        """
        Convert the data points list into a pandas DataFrame.

        Parameters
        ----------
        column_names : {name, id}
            Which field to use as column header. Defaults to 'name'.

        Returns
        -------
        pandas.DataFrame
            The dataframe.
        """
        dfs = [dps.to_pandas(column_name=column_names) for dps in self]
        if dfs:
            df = pd.concat(dfs, axis="columns")
            return df
        else:
            return pd.DataFrame()
