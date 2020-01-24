"""
Configurations.
"""
import os


class Config(object):
    datetime_format = "%Y-%m-%dT%H:%M:%S.%fZ"  # example datetime string "2019-10-14T09:46:49.606Z"
    base_url = "api.gateway.equinor.com/plant"
    idp_base_url = "login.microsoftonline.com"
    idp_tenant = os.getenv("EquinorAzureADTenantId", "3aa4a235-b6e2-48d5-9195-7fcf05b459b0")
    default_resource_id = "141369bd-3dca-4b55-825b-56ad4a69b1fc"
    default_client_id = "67da184b-6bde-43fd-a155-30ed4ff162d2"
    log_level = "info"


class TestConfig(Config):
    base_url = "api.gateway.equinor.com/plant-beta"
