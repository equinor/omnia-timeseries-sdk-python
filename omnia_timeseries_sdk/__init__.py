"""
Omnia Python SDK
"""
from pkg_resources import get_distribution, DistributionNotFound
from .client import OmniaClient


__summary__ = __doc__

# get version
try:
    # version at runtime from distribution/package info
    __version__ = get_distribution("omnia_timeseries_sdk").version
except DistributionNotFound:
    # package is not installed
    __version__ = ""
