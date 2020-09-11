import os
import sys

from hfr_app.adapters.google_adapter import GooglePubSubAdapter
from hfr_app.adapters.ports import FeederCommunicationPort


class Settings(object):
    feeder_communication: FeederCommunicationPort = None


class GoogleSettings(Settings):
    feeder_communication = GooglePubSubAdapter


def get_settings() -> Settings:
    cls_prefix = str.capitalize(os.environ.get("SETTINGS", "Default"))
    cls_name = f"{cls_prefix}Settings"
    return getattr(sys.modules[__name__], cls_name)
