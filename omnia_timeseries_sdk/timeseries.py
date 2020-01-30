"""
Timeseries API
"""
import datetime
from typing import List
from .resources import DataPoint, DataPoints, TimeSeries, TimeSeriesList
from ._utils import to_omnia_datetime_string


class TimeSeriesAPI(object):
    """
    Timeseries API client

    Parameters
    ----------
    omnia_client : OmniaClient
        Omnia client
    """
    _resource_path = "timeseries"
    _api_version = "v1.5"

    def __init__(self, omnia_client):
        self._omnia_client = omnia_client

    def create(self, name: str, description: str = None, asset_id: str = None, unit: str = None,
               external_id: str = None, step: bool = False):
        """
        Create a single timeseries object.

        Parameters
        ----------
        name : str
            Name of the timeseries.
        description : str, optional
            Description of the timeseries.
        asset_id : str, optional
            ID of the asset this timeseries belongs to.
        unit : str, optional
            The timeseries physical unit of measure.
        external_id : str, optional
            ID from another (external) system provided by client.
        step : bool, optional
            Is this a step time series.

        Returns
        -------
        TimeSeries
            Time series instance.

        """
        # only name is mandatory
        body = dict(name=name, description=description, step=step, unit=unit, asset_id=asset_id,
                    external_id=external_id)
        items = self._omnia_client.post(self._resource_path, self._api_version, "", body=body)
        return TimeSeries(**items[0], omnia_client=self._omnia_client)

    def update(self, id: str, name: str = None, description: str = None, asset_id: str = None, unit: str = None,
               external_id: str = None, step: bool = False):
        """
        Update a single timeseries object.

        Parameters
        ----------
        id : str
            Id of the timeseries to update
        name : str, optional
            Name of the timeseries.
        description : str, optional
            Description of the timeseries.
        asset_id : str, optional
            ID of the asset this timeseries belongs to.
        unit : str, optional
            The timeseries physical unit of measure.
        external_id : str, optional
            ID from another (external) system provided by client.
        step : bool, optional
            Is this a step time series.

        Returns
        -------
        TimeSeries
            Time series instance.

        """
        # only name is mandatory
        body = dict(name=name, description=description, step=step, unit=unit, asset_id=asset_id,
                    external_id=external_id)
        items = self._omnia_client.patch(self._resource_path, self._api_version, id, body=body)
        return TimeSeries(**items[0], omnia_client=self._omnia_client)

    def delete(self, id: str):
        """
        Delete time series with given id.

        Parameters
        ----------
        id : str
            Time series id.

        """
        return self._omnia_client.delete(self._resource_path, self._api_version, id)

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

    def search(self):
        raise NotImplementedError

    def add_data(self, id: str, time: List, values: List, status: List, asynch: bool = False):
        """
        Add or update a timeseries' datapoints.

        Parameters
        ----------
        id : str
            Id of timeseries for which to add or update datapoints.
        time : List[datetime.datetime]
            Datetime of each datapoint.
        values : List[Union[float, int, str]]
            Value of each datapoint.
        status : List[int]
            Status of each datapoint.
        asynch : bool, optional
            Determines whether the datapoints should be added or updated asynchronoulsy. If you set this to true only
            permission check will be performed and 202 Accepted will be returned. If you set this to false or do not
            supply it, the request will not be returned until the changes are committed.

        """
        if not len(time) == len(values) == len(status):
            raise ValueError("The number of items in `time`, `value` and `status` must be equal.")

        parameters = {"async": asynch}
        body = dict(datapoints=[dict(time=to_omnia_datetime_string(t), value=v, status=s) for t, v, s in zip(time, values, status)])
        _ = self._omnia_client.post(self._resource_path, self._api_version, f"{id}/data", parameters=parameters,
                                    body=body)

    def add_data_on_multiple(self, id: str):
        raise NotImplementedError

    def delete_data(self, id: str, start_time: str = None, end_time: str = None):
        """
        Delete datapoints from a timeseries.

        Parameters
        ----------
        id : str
            Id of timeseries for which to delete data.
        start_time : str, optional
            Format - date-time (as date-time in RFC3339). Inclusive start bound of deletion window.
        end_time : str, optional
            Format - date-time (as date-time in RFC3339). Non-inclusive end bound of deletion window.

        """
        parameters = dict(start_time=start_time, end_time=end_time)
        _ = self._omnia_client.delete(self._resource_path, self._api_version, f"{id}/data", parameters=parameters)

    def data(self, id: str, start_time: str = None, end_time: str = None, limit=None, include_outside_points: bool = False):
        """
        Retrieves datapoints in a given time window according to applied parameters.

        Parameters
        ----------
        id : str
            Time series id
        start_time: str, optional
            Start of data window, date-time in ISO format (RFC3339), defaults to 1 day ago.
        end_time: str, optional
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
        if end_time is None:
            end_time = to_omnia_datetime_string(datetime.datetime.utcnow())
        if start_time is None:
            start_time = to_omnia_datetime_string(datetime.datetime.utcnow() - datetime.timedelta(days=1))

        parameters = dict(start_time=start_time, end_time=end_time, limit=limit, include_outside_points=include_outside_points)
        items = self._omnia_client.get(self._resource_path, self._api_version, f"{id}/data", parameters=parameters)
        ts = items[0]   # should be only 1 time series
        id = ts.get("id")
        name = ts.get("name")
        unit = ts.get("unit")
        dps = ts.get("datapoints")
        time = [dp.get("time") for dp in dps]
        value = [dp.get("value") for dp in dps]
        return DataPoints(id=id, name=name, unit=unit, time=time, value=value, omnia_client=self._omnia_client)

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
        return DataPoint(id=id, name=name, unit=unit, **dp, omnia_client=self._omnia_client)

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
        return DataPoint(id=id, name=name, unit=unit, **dp, omnia_client=self._omnia_client)




