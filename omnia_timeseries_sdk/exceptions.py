"""
Omnia Timeseries exceptions.
"""


class OmniaAuthenticationError(Exception):
    """
    Omnia Timeseries API authentication error.

    Raised if the API authentication fails. Either credentials are missing or invalid.
    """
    pass


class OmniaClientConnectionError(Exception):
    """
    Omnia timeseries API client connection error.

    Raised if the https connection fails.
    """
    pass


class OmniaTimeSeriesAPIError(Exception):
    def __init__(self, status, reason, msg):
        self.status = status
        self.reason = reason
        self.msg = msg

    def __str__(self):
        return f"[{self.status}] {self.reason}. {self.msg}."

