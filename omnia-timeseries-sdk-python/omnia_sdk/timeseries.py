"""
Timeseries API
"""
import datetime
import logging
from typing import Union
from ._config import _DATETIME_FORMAT
from ._base import OmniaResource, OmniaResourceList


class TimeSeriesAPI(object):
    """
    Timeseries API client

    Parameters
    ----------
    omnia_client : OmniaClient
        Omnia client
    """
    _resource_path = "plant/timeseries"
    _api_version = "v1.3"

    def __init__(self, omnia_client):
        self._omnia_client = omnia_client

    @staticmethod
    def _unpack_response(response):
        """
        Unpack request response.

        Parameters
        ----------
        response : dict
            Response from request.

        Returns
        -------

        """
        # TODO: Consider to move this to utilities if it the response structure is generic across endpoints
        try:
            items = response.get('data').get('items', list())
        except AttributeError:
            return list()
        else:
            return items

    def list(self, name: str=None, external_id: str=None, asset_id: str=None, limit: int=None, skip: int=None,
             continuation_token: str=None):
        """
        List over all timeseries.

        Parameters
        ----------
        name : str, optional
            Name of the timeseries
        external_id : str, optional
            ID from another (external) system provided by client
        asset_id : str, optional
            ID of the asset this timeseries belongs to
        limit : int, optional
            Limit the number of results to retrieve, between 1-1000.
        skip : int, optional
            Retrieve results except the `skip` first ones.
        continuation_token : str, optional
            The continuation_token for next result set

        Returns
        -------
        TimeSeriesList
            List of time series resources.

        Notes
        -----
        The web API uses camelcase parameters.

        """
        _ = dict(name=name, externalId=external_id, assetId=asset_id, limit=limit, skip=skip,
                 continuationToken=continuation_token)
        parameters = {k: v for k, v in _.items() if v is not None}
        return self._omnia_client._get(self._resource_path, self._api_version, "", parameters=parameters)

    def retrieve(self, id: str):
        """
        Retrieve a single time series by id.

        Parameters
        ----------
        id : str
            Time series id.
        """
        items = self._unpack_response(self._omnia_client._get(self._resource_path, self._api_version, id))
        if len(items) == 0:
            logging.info(f"Could not find time series with id={id}.")
        elif len(items) > 1:
            logging.warning(f"Found {len(items)} with id={id}. Using the first one.")
        else:
            pass

        return TimeSeries(**items[0], omnia_client=self._omnia_client)

    def retrieve_multiple(self, ids: list):
        """
        Retrieve multiple time series by id.

        Parameters
        ----------
        ids : list[str]
            Times series id.

        """
        # TODO: Update when Timeseries API support retrieving multiple timeseries by id
        timeseries = [self.retrieve(id) for id in ids]
        return TimeSeriesList(timeseries, omnia_client=self._omnia_client)

    def data(self, id: str, start: str = None, end: str = None, limit=None, include_outside_points: bool = False):
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
        if end is None:
            end = datetime.datetime.now().isoformat()
        if start is None:
            start = (end - datetime.timedelta(days=1)).isoformat()
        _ = dict(startTime=start, endTime=end, limit=limit, includeOutsidePoints=include_outside_points)
        parameters = {k: v for k, v in _.items() if v is not None}
        items = self._unpack_response(
            self._omnia_client._get(
                self._resource_path, self._api_version, f"{id}/data", parameters=parameters
            )
        )
        return DataPoints(items.get('datapoints'))

    def first_data(self, id: str):
        raise NotImplementedError

    def latest_data(self, id: str):
        raise NotImplementedError

    def count_data(self, id: str):
        raise NotImplementedError

    def create(self):
        raise NotImplementedError

    def delete(self):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def search(self):
        raise NotImplementedError


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
                 asset_id: str = None, omnia_client=None):
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
    """
    def __init__(self, timeseries: list, omnia_client=None):
        self.resources = timeseries
        self._omnia_client = omnia_client

    def plot(self):
        raise NotImplementedError


class DataPoint(OmniaResource):
    """
    An object representing a data point.
    """
    def __init__(self, time: str=None, value: Union[int, float]=None, status: int=None):
        self.time = time
        self.value = value
        self.status = status

    def dump(self):
        """
        Dump the instance into a json serializable Python data type.

        Returns
        -------
        Dict[str, Any]
            A dictionary representation of the instance.
        """
        return {key: value for key, value in self.__dict__.items() if value is not None and not key.startswith("_")}


class DataPoints(object):
    """
    An object representing a list of data points.
    """