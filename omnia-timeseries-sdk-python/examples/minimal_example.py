"""
OMNIA Timeseries API example
"""
import os
import json
import pprint
import datetime
import http.client
import adal


BASE_URL = "api.gateway.equinor.com"
IDP_BASE_URL = "login.microsoftonline.com"
TENANT = "3aa4a235-b6e2-48d5-9195-7fcf05b459b0"


def request_token_adal():
    """Requests token using ADAL."""
    resource = os.getenv("resource")
    client_id = os.getenv("clientId")
    client_secret = os.getenv("clientSecret")
    if not resource or not client_id or not client_secret:
        print("Credentials are not provided.")
        return

    current_resource_id = os.getenv("currentResourceId")
    current_client_id = os.getenv("currentClientId")
    token_expires_on = os.getenv("accessTokenExpiry")
    if (current_resource_id == resource and current_client_id == client_id and token_expires_on is not None
            and datetime.datetime.now().timestamp() < float(token_expires_on) * 1000):
        print("Current access token is still valid.")
        return

    context = adal.AuthenticationContext(f'https://{IDP_BASE_URL}/{TENANT}', validate_authority=(TENANT != 'adfs'))
    try:
        data = context.acquire_token_with_client_credentials(resource, client_id, client_secret)
    except adal.adal_error.AdalError as e:
        print("Unable to aquire access token.")
        return
    else:
        print("Aquired access token.")
        os.environ["currentAccessToken"] = data.get("accessToken")
        os.environ["accessTokenExpiry"] = str(datetime.datetime.strptime(data.get("expiresOn"), "%Y-%m-%d %H:%M:%S.%f").timestamp())
        os.environ["currentClientId"] = data.get("_clientId")
        os.environ["currentResourceId"] = data.get("resource")
        os.environ["tokenExpiryDate"] = data.get("expiresOn")


def omnia_timeseries_list():
    """List available timeseries in OMNIA"""
    headers = dict(Authorization=f"Bearer {os.getenv('currentAccessToken', '')}")

    try:
        connection = http.client.HTTPSConnection(BASE_URL)
        connection.request("GET", "/plant/timeseries/v1.3/?limit=5", headers=headers)
    except Exception as e:
        print(str(e))
    else:
        response = connection.getresponse()
        data = json.loads(response.read())
        pprint.pprint(data)


if __name__ == "__main__":
    request_token_adal()
    omnia_timeseries_list()
    request_token_adal()

