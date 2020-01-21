"""
Timeseries API
"""
import logging
import datetime
from .resources import DataPoint, DataPoints, TimeSeries, TimeSeriesList


class TimeSeriesAPI(object):
    """
    Timeseries API client

    Parameters
    ----------
    omnia_client : OmniaClient
        Omnia client
    """
    _resource_path = "plant/timeseries"
    _api_version = "v1.5"

    def __init__(self, omnia_client):
        self._omnia_client = omnia_client

    def list(self, name: str = None, external_id: str = None, asset_id: str = None, limit: int = None, skip: int = None,
             continuation_token: str = None):
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
        parameters = dict(name=name, external_id=external_id, asset_id=asset_id, limit=limit, skip=skip,
                          continuation_token=continuation_token)
        items = self._omnia_client.get(self._resource_path, self._api_version, "", parameters=parameters)
        return TimeSeriesList([TimeSeries(**item, omnia_client=self._omnia_client) for item in items])

    def retrieve(self, id: str):
        """
        Retrieve a single time series by id.

        Parameters
        ----------
        id : str
            Time series id.

        Returns
        -------
        TimeSeries
            Time series instance.

        """
        items = self._omnia_client.get(self._resource_path, self._api_version, id)
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

        Returns
        -------
        TimeSeriesList
            List of time series instances

        """
        # TODO: Update when Timeseries API support retrieving multiple timeseries by id
        timeseries = [self.retrieve(id) for id in ids]
        return TimeSeriesList(timeseries, omnia_client=self._omnia_client)

    def update(self):
        raise NotImplementedError

    def search(self):
        raise NotImplementedError

    def add_data(self, id: str):
        raise NotImplementedError

    def add_data_on_multiple(self, id: str):
        raise NotImplementedError

    def delete_data(self, id: str):
        raise NotImplementedError

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
            Limit of datapoints to retrieve from within the time window. Between 1-100 000. The default value is 1000.
        include_outside_points: bool, optional
            Determines whether or not the points immediately prior to and following the time window should be
            included in result.

        Returns
        -------
        DataPoints
            Time series data points in time window.

        """
        if end is None:
            end = datetime.datetime.utcnow().isoformat()
        if start is None:
            start = (datetime.datetime.utcnow() - datetime.timedelta(days=1)).isoformat()

        parameters = dict(start_time=start, end_time=end, limit=limit, include_outside_points=include_outside_points)
        items = self._omnia_client.get(self._resource_path, self._api_version, f"{id}/data", parameters=parameters)
        ts = items[0]   # should be only 1 time series
        id = ts.get("id")
        name = ts.get("name")
        unit = ts.get("unit")
        dps = ts.get("datapoints")
        time = [dp.get("time") for dp in dps]
        value = [dp.get("value") for dp in dps]
        return DataPoints(id=id, name=name, unit=unit, time=time, value=value)

    def first_data(self, id: str, after_time: str = None):
        """
        Retrieves the first data point of a time series.

        Parameters
        ----------
        id : str
            Id of time series from which to retrieve data.
        after_time : str, optional
            ISO formatted date-time string. Only look for data points after this time.

        Returns
        -------
        DataPoint
            The data point.

        """
        parameters = dict(after_time=after_time)
        items = self._omnia_client.get(self._resource_path, self._api_version, f"{id}/data/first",
                                       parameters=parameters)
        ts = items[0]  # should be only 1 time series
        id = ts.get("id")
        name = ts.get("name")
        unit = ts.get("unit")
        dp = ts.get("datapoints")[0]
        return DataPoint(id=id, name=name, unit=unit, **dp)

    def latest_data(self, id: str, before_time: str = None):
        """
        Retrieves the latest data point of a time series.

        Parameters
        ----------
        id : str
            Id of time series from which to retrieve data.
        before_time : str, optional
            ISO formatted date-time string. Only look for data points before this time.

        Returns
        -------
        DataPoint
            The data point.
        """
        parameters = dict(before_time=before_time)
        items = self._omnia_client.get(self._resource_path, self._api_version, f"{id}/data/latest",
                                       parameters=parameters)
        ts = items[0]  # should be only 1 time series
        id = ts.get("id")
        name = ts.get("name")
        unit = ts.get("unit")
        dp = ts.get("datapoints")[0]
        return DataPoint(id=id, name=name, unit=unit, **dp)




