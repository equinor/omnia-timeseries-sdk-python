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
from ._config import BASE_URL, IDP_BASE_URL, DEFAULT_TENANT
from ._utils import to_snake_case

TENANT = os.getenv("EquinorAzureADTenantId", DEFAULT_TENANT)


class OmniaClient(object):
    """
    Main entrypoint into Omnia Python SDK.

    Parameters
    ----------
    base_url : str, optional
        Base url to send requests to, defaults to "https://api.gateway.equinor.com"
    log_level : {debug, info, error}
        Set logging severity level.

    Notes
    -----
    These environmental variables must be set if authenticating by user impersonation
        omniaClientId - Client identifier
        omniaResourceId - Omnia resource identifier

    Additionally you must set this environmental variable if authenticating with a shared secret (machine-to-machine)
        omniaClientSecret - Shared secret key

    """
    def __init__(self, base_url: str = None, log_level: str = None):
        self.base_url = base_url or BASE_URL
        self.time_series = TimeSeriesAPI(omnia_client=self)

        log_levels = dict(debug=logging.DEBUG, info=logging.INFO, error=logging.ERROR)
        logging.basicConfig(stream=sys.stdout,
                            level=log_levels.get(log_level, logging.INFO),
                            format="%(levelname)s at line %(lineno)d in %(filename)s - %(message)s")

    @staticmethod
    def _token_request():
        """Requests access token."""
        # Set resource id and client id. Default ids for authentication by user impersonation (without shared secret).
        # service-to-service / machine-to-machine authentication using a shared secret requires generally different
        # resource and client ids and a shared secret (client secret). See also
        # https://github.com/equinor/OmniaPlant/wiki/Authentication-&-Authorization
        resource_id = os.getenv("omniaResourceId", "141369bd-3dca-4b55-825b-56ad4a69b1fc")
        client_id = os.getenv("omniaClientId", "67da184b-6bde-43fd-a155-30ed4ff162d2")
        client_secret = os.getenv("omniaClientSecret")

        # check if current access token is still valid
        current_resource_id = os.getenv("currentOmniaResourceId")
        current_client_id = os.getenv("currentOmniaClientId")
        token_expires_on = os.getenv("omniaAccessTokenExpiry")
        if (current_resource_id == resource_id and current_client_id == client_id and token_expires_on is not None
                and datetime.datetime.now().timestamp() < float(token_expires_on) * 1000):
            logging.debug("Current access token is still valid.")
            return

        context = adal.AuthenticationContext(f'https://{IDP_BASE_URL}/{TENANT}')
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
            return
        else:
            os.environ["currentOmniaAccessToken"] = data.get("accessToken")
            os.environ["omniaAccessTokenExpiry"] = str(
                datetime.datetime.strptime(data.get("expiresOn"), "%Y-%m-%d %H:%M:%S.%f").timestamp())
            os.environ["currentOmniaClientId"] = data.get("_clientId")
            os.environ["currentOmniaResourceId"] = data.get("resource")
            os.environ["omniaAccessTokenExpiryDate"] = data.get("expiresOn")
            logging.debug("Acquired valid access token.")

    def _delete(self, resource: str, version: str, endpoint: str, parameters: dict = None, body: dict = None):
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
        return self._do_request("DELETE", resource, endpoint, version, parameters=parameters, body=body)

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

        url = "/" + "/".join([p for p in [resource, version, endpoint] if p.strip()])
        if parameters is not None and isinstance(parameters, dict):
            enc_parameters = urllib.parse.urlencode(parameters)
            limit = parameters.get("limit")
        else:
            enc_parameters = ""
            limit = None

        url_with_parameters = f"{url}/?{enc_parameters}"
        headers = dict(
            Authorization=f"Bearer {os.getenv('currentOmniaAccessToken', '')}",
            Connection="keep-alive",
            Host=BASE_URL,
        )
        if body is not None:
            headers["Content-Type"] = "application/json; charset=utf=8"

        msg = f"{method.upper()} {url_with_parameters} {http.client.__doc__.split()[0]}"
        for k, v in headers.items():
            msg += f"\n{k}: {v}"

        if body is not None:
            msg += f"\nBody:\n{json.dumps(body, indent=2)}"

        logging.debug(msg)

        try:
            connection = http.client.HTTPSConnection(self.base_url)
        except Exception:
            logging.error("Request failed", exc_info=True)
            return

        results = list()
        query_url = url_with_parameters
        n_items = 0
        while True:
            connection.request(method, query_url, body=json.dumps(body), headers=headers)
            r = connection.getresponse()
            if not r.status == 200:
                logging.error(f"Request failed. [{r.status}] {r.reason}")
                break
            else:
                _ = json.loads(r.read())
                continuation_token = _.get("continuationToken")
                items = _.get("data").get("items")
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

    def _get(self, resource: str, version: str, endpoint: str, parameters: dict = None, body: dict = None):
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

    def _patch(self, resource: str, version: str, endpoint: str, parameters: dict = None, body: dict = None):
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

    def _post(self, resource: str, version: str, endpoint: str, parameters: dict = None, body: dict = None):
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

    def _put(self, resource: str, version: str, endpoint: str, parameters: dict = None, body: dict = None):
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

