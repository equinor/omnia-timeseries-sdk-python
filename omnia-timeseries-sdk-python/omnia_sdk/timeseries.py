"""
Timeseries API
"""
import json
import datetime
import logging
from ._config import _DATETIME_FORMAT
from ._utils import make_serializable


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

    def list(self, **kwargs):
        """
        List over all timeseries.

        Parameters
        ----------
        name : str, optional
            Name of the timeseries
        externalId : str, optional
            ID from another (external) system provided by client
        assetId : str, optional
            ID of the asset this timeseries belongs to
        limit : int, optional
            Limit the number of results to retrieve, between 1-1000.
        skip : int, optional
            Retrieve results except the `skip` first ones.
        continuationToken : str, optional
            The continuationToken for next result set

        Returns
        -------
        TimeSeriesList
            List of time series resources.

        Notes
        -----
        The web API uses camelcase parameters.

        """
        _ALLOWED = ["name", "externalId", "assetId", "limit", "skip", "continuationToken"]
        endpoint = ""
        parameters = {k: v for k, v in kwargs.items() if k in _ALLOWED and v is not None}
        return self._omnia_client._get(self._resource_path, self._api_version, endpoint, parameters=parameters)

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

    def create(self):
        raise NotImplementedError

    def delete(self):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def search(self):
        raise NotImplementedError


class TimeSeries(object):
    """
    Timeseries resource

    Parameters
    ----------

    """
    def __init__(self, id: str = None, externalId: str = None, name: str = None, description: str = None,
                 step: bool = None, unit: str = None, createdTime: str = None, changedTime: str = None,
                 assetId: str = None, omnia_client=None):

        self.id = id
        self.externalId = externalId
        self.assetId = assetId
        self.name = name
        self.description = description
        self.step = step
        self.unit = unit
        self.createdTime = datetime.datetime.strptime(createdTime, _DATETIME_FORMAT)
        self.changedTime = datetime.datetime.strptime(changedTime, _DATETIME_FORMAT)
        self._omnia_client = omnia_client

    def __str__(self):
        return json.dumps(make_serializable(self.dump()), indent=2)

    def __repr__(self):
        return self.__str__()

    def count(self):
        """int: Number of datapoints in this time series."""
        pass

    def dump(self):
        """
        Dump the instance into a json serializable Python data type.

        Returns
        -------
        Dict[str, Any]
            A dictionary representation of the instance.
        """
        return {key: value for key, value in self.__dict__.items() if value is not None and not key.startswith("_")}

    def latest(self):
        """DataPoint: Latest data point in time series."""
        pass

    def first(self):
        """DataPoint: First data point in time series."""
        pass

    def plot(self, start=None, end=None, aggregates=None, granularity=None, *args, **kwargs):
        """
        PLot time series
        """
        # TODO: pandas
        pass


class TimeSeriesList(object):
    """
    List of TimeSeries
    """
    def __init__(self, data: list, omnia_client=None):
        self.data = data
        self._omnia_client = omnia_client

    def dump(self):
        """
        Dump the instance into a json serializable Python data type.

        Returns
        -------
        List[Dict[str, Any]]
            A list of dicts representing the instance.
        """
        return [resource.dump() for resource in self.data]

    def plot(self):
        pass
