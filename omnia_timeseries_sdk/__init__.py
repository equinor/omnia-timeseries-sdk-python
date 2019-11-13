"""
Python SDK for Omnia Timeseries API
"""
from pkg_resources import get_distribution, DistributionNotFound
from .client import OmniaClient


try:
    # version at runtime from distribution/package info
    __version__ = get_distribution("omnia_timeseries_sdk").version
except DistributionNotFound:
    # package is not installed
    __version__ = ""
