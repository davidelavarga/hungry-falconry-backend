from hfr_app.adapters.ports import FeederCommunicationPort
from jsonschema import validate
from hfr_app.json_schemas import publish_schedule_schema


class GooglePubSubAdapter(FeederCommunicationPort):
    def publish_schedule_request(self, schedule_data: dict, auth_token: str):
        schedule_data["auth_token"] = auth_token
        schedule_data["id"] = str(schedule_data["id"])
        validate(instance=schedule_data, schema=publish_schedule_schema)
        # Send to PubSub
