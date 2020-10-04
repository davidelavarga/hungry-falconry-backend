import os
import sys

from hfr_app.adapters.google_adapter import GooglePubSubAdapter, GoogleSecretManager
from hfr_app.adapters.ports import FeederCommunicationPort, SecretsStorePort


class Settings(object):
    feeder_communication: FeederCommunicationPort = None
    secret_store: SecretsStorePort = None


class GoogleSettings(Settings):
    feeder_communication = GooglePubSubAdapter
    secret_store = GoogleSecretManager


class DefaultSettings(Settings):
    feeder_communication = GooglePubSubAdapter
    secret_store = GoogleSecretManager


def get_settings() -> Settings:
    cls_prefix = str.capitalize(os.environ.get("SETTINGS", "Default"))
    cls_name = f"{cls_prefix}Settings"
    return getattr(sys.modules[__name__], cls_name)
