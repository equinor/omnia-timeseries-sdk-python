"""
Omnia client.
"""
import os
import sys
import logging
import json
import datetime
import adal
import http.client
import urllib.parse
import urllib.error
from .timeseries import TimeSeriesAPI
from ._config import Config
from ._utils import to_snake_case, to_camel_case
from .exceptions import OmniaAuthenticationError, OmniaClientConnectionError, OmniaTimeSeriesAPIError


class OmniaClient(object):
    """
    Main entrypoint into Omnia Python SDK.

    Parameters
    ----------
    config : object, optional
        Client configuration (base url, IDP tenant, date-time format, logging level etc.)

    Notes
    -----
    These environmental variables must be set if authenticating by user impersonation
        omniaClientId - Client identifier
        omniaResourceId - Omnia resource identifier

    Additionally you must set this environmental variable if authenticating with a shared secret (machine-to-machine)
        omniaClientSecret - Shared secret key

    """
    def __init__(self, config=Config):
        self.config = config
        self.time_series = TimeSeriesAPI(omnia_client=self)

        log_levels = dict(debug=logging.DEBUG, info=logging.INFO, error=logging.ERROR)
        logging.basicConfig(stream=sys.stdout,
                            level=log_levels.get(self.config.log_level, logging.INFO),
                            format="%(levelname)s at line %(lineno)d in %(filename)s - %(message)s")

    @property
    def idp_url(self):
        """str: Identity provider URL."""
        return f'https://{self.config.idp_base_url}/{self.config.idp_tenant}'

    def _token_request(self):
        """Requests access token."""
        # Set resource id and client id. Default ids for authentication by user impersonation (without shared secret).
        # service-to-service / machine-to-machine authentication using a shared secret requires generally different
        # resource and client ids and a shared secret (client secret). See also
        # https://github.com/equinor/OmniaPlant/wiki/Authentication-&-Authorization
        resource_id = os.getenv("omniaResourceId", self.config.default_resource_id)
        client_id = os.getenv("omniaClientId", self.config.default_client_id)
        client_secret = os.getenv("omniaClientSecret")

        # check if current access token is still valid
        current_resource_id = os.getenv("currentOmniaResourceId")
        current_client_id = os.getenv("currentOmniaClientId")
        token_expires_on = os.getenv("omniaAccessTokenExpiry")
        if (current_resource_id == resource_id and current_client_id == client_id and token_expires_on is not None
                and datetime.datetime.now().timestamp() < float(token_expires_on) * 1000):
            logging.debug("Current access token is still valid.")
            return

        context = adal.AuthenticationContext(self.idp_url)
        try:
            if client_secret is not None:
                logging.info("Authenticating with shared client secret (service-to-service).")
                data = context.acquire_token_with_client_credentials(resource_id, client_id, client_secret)
            else:
                logging.info("Authenticating by user impersonation without any shared secret.")
                code = context.acquire_user_code(resource_id, client_id)
                print(f"\nUSER INTERACTION REQUIRED\n{code['message']}\n")
                data = context.acquire_token_with_device_code(resource_id, code, client_id)
        except adal.adal_error.AdalError as e:
            logging.error("Unable to acquire a valid access token.", exc_info=True)
            raise OmniaAuthenticationError()
        else:
            os.environ["currentOmniaAccessToken"] = data.get("accessToken")
            os.environ["omniaAccessTokenExpiry"] = str(
                datetime.datetime.strptime(data.get("expiresOn"), "%Y-%m-%d %H:%M:%S.%f").timestamp())
            os.environ["currentOmniaClientId"] = data.get("_clientId")
            os.environ["currentOmniaResourceId"] = data.get("resource")
            os.environ["omniaAccessTokenExpiryDate"] = data.get("expiresOn")
            logging.debug("Acquired valid access token.")

    def _do_request(self, method: str, resource: str, version: str, endpoint: str, parameters: dict = None,
                    body: dict = None):
        """
        Carry out request.

        Parameters
        ----------
        method : {'GET', 'POST', 'PUT', 'PATCH', 'DELETE'}
            Request method.
        resource : str
            API resource e.g. 'plant/timeseries'
        version : str
            API version e.g. 'v1.3'
        endpoint : str
            API resource endpoint e.g.
        parameters : dict, optional
            Request parameters.
        body : dict, optional
            Request body.

        Returns
        -------
        dict
            Request response

        Notes
        -----
        The full request url is like
            'https://{base_url}/{resource}/{version}?firstparameter=value&anotherparameter=value

        """
        # request new access token
        self._token_request()

        url = "/" + "/".join([p for p in [self.config.base_url, resource, version, endpoint] if p.strip()])
        if parameters is not None and isinstance(parameters, dict):
            parameters = to_camel_case({k: v for k, v in parameters.items() if v is not None})
            enc_parameters = urllib.parse.urlencode(parameters)
            limit = parameters.get("limit")
        else:
            enc_parameters = ""
            limit = None

        url_with_parameters = f"{url}/?{enc_parameters}"
        headers = dict(
            Authorization=f"Bearer {os.getenv('currentOmniaAccessToken', '')}",
            Connection="keep-alive",
            Host=self.config.host,
        )

        msg = f"{method.upper()} {url_with_parameters} {http.client.__doc__.split()[0]}"
        for k, v in headers.items():
            msg += f"\n{k}: {v}"

        if body is not None:
            body = to_camel_case({k: v for k, v in body.items() if v is not None})
            headers["Content-Type"] = "application/json"
            msg += f"\nBody:\n{json.dumps(body, indent=2)}"

        logging.debug(msg)

        try:
            connection = http.client.HTTPSConnection(self.config.host)
        except Exception:
            logging.error("Request failed", exc_info=True)
            raise OmniaClientConnectionError()

        results = list()
        query_url = url_with_parameters
        n_items = 0
        while True:
            connection.request(method, query_url, body=json.dumps(body), headers=headers)
            r = connection.getresponse()
            response = json.loads(r.read())
            msg = response.get("message") or ""

            if not r.status == 200:
                logging.error(f"Request failed. [{r.status}] {r.reason}. {msg}.")
                raise OmniaTimeSeriesAPIError(r.status, r.reason, msg)
            else:
                logging.debug(f"Request succeded. [{r.status}] {r.reason}. {msg}.")
                if response.get("data") is None:
                    return
                else:
                    continuation_token = response.get("continuationToken")
                    items = response.get("data").get("items")

                    if items is None or len(items) == 0:
                        break

                    results.extend(items)

                    if items[0].get("datapoints") is not None:
                        # limit response size based on number of returned data points
                        # TODO: Not robust because the web API return datapoints as
                        #  {"data": {"items": [{"datapoints": [{"time": ..., "value": ..., "status: ...}]}, ]}} under items.
                        #  Should rather return datapoints directly under "items" to be generic, like
                        #  {"data": {"items": [{"time": ..., "value": ..., "status: ...}, {...}, {...}]}}
                        n_items += len(items[0].get("datapoints"))
                    else:
                        n_items += len(items)

                    if continuation_token is None or (limit is not None and n_items >= limit):
                        break
                    else:
                        query_url = f"{url_with_parameters}&continuationToken={continuation_token}"
                        logging.debug(f"\tFetching next page... {query_url}")

        connection.close()
        return to_snake_case(results)

    def delete(self, resource: str, version: str, endpoint: str, parameters: dict = None, body: dict = None):
        """
        DELETE request

        Parameters
        ----------
        resource : str
            API resource e.g. 'plant/timeseries'
        endpoint : str
            API resource endpoint e.g.
        version : str
            API version e.g. 'v1.3'
        parameters : dict, optional
            Request parameters.
        body : dict, optional
            Request body.

        Returns
        -------
        dict
            Request response

        Notes
        -----
        The full request url is like
            'https://{base_url}/{resource}/{version}?firstparameter=value&anotherparameter=value

        """
        return self._do_request("DELETE", resource, version, endpoint, parameters=parameters, body=body)

    def get(self, resource: str, version: str, endpoint: str, parameters: dict = None, body: dict = None):
        """
        GET request

        Parameters
        ----------
        resource : str
            API resource e.g. 'plant/timeseries'
        version : str
            API version e.g. 'v1.3'
        endpoint : str
            API resource endpoint e.g.
        parameters : dict, optional
            Request parameters.
        body : dict, optional
            Request body.

        Returns
        -------
        dict
            Request response

        Notes
        -----
        The full request url is like
            'https://{base_url}/{resource}/{version}?firstparameter=value&anotherparameter=value

        """
        return self._do_request("GET", resource, version, endpoint, parameters=parameters, body=body)

    def patch(self, resource: str, version: str, endpoint: str, parameters: dict = None, body: dict = None):
        """
        POST request

        Parameters
        ----------
        resource : str
            API resource e.g. 'plant/timeseries'
        version : str
            API version e.g. 'v1.3'
        endpoint : str
            API resource endpoint e.g.
        parameters : dict, optional
            Request parameters.
        body : dict, optional
            Request body.

        Returns
        -------
        dict
            Request response

        Notes
        -----
        The full request url is like
            'https://{base_url}/{resource}/{version}?firstparameter=value&anotherparameter=value

        """
        return self._do_request("PATCH", resource, version, endpoint, parameters=parameters, body=body)

    def post(self, resource: str, version: str, endpoint: str, parameters: dict = None, body: dict = None):
        """
        POST request

        Parameters
        ----------
        resource : str
            API resource e.g. 'plant/timeseries'
        version : str
            API version e.g. 'v1.3'
        endpoint : str
            API resource endpoint e.g.
        parameters : dict, optional
            Request parameters.
        body : dict, optional
            Request body.

        Returns
        -------
        dict
            Request response

        Notes
        -----
        The full request url is like
            'https://{base_url}/{resource}/{version}?firstparameter=value&anotherparameter=value

        """
        return self._do_request("POST", resource, version, endpoint, parameters=parameters, body=body)

    def put(self, resource: str, version: str, endpoint: str, parameters: dict = None, body: dict = None):
        """
        PUT request

        Parameters
        ----------
        resource : str
            API resource e.g. 'plant/timeseries'
        version : str
            API version e.g. 'v1.3'
        endpoint : str
            API resource endpoint e.g.
        parameters : dict, optional
            Request parameters.
        body : dict, optional
            Request body.

        Returns
        -------
        dict
            Request response

        Notes
        -----
        The full request url is like
            'https://{base_url}/{resource}/{version}?firstparameter=value&anotherparameter=value

        """
        return self._do_request("PUT", resource, version, endpoint, parameters=parameters, body=body)

