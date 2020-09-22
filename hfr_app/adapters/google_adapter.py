import os
import json
from hfr_app.adapters.ports import FeederCommunicationPort
from google.cloud import pubsub_v1

GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
PROJECT_ID = os.getenv("PROJECT_ID")
TOPIC_ID = os.getenv("TOPIC_ID")


class GooglePubSubAdapter(FeederCommunicationPort):

    def __init__(self):
        self.publisher = pubsub_v1.PublisherClient()
        self.topic_path = self.publisher.topic_path(PROJECT_ID, TOPIC_ID)

    def publish_schedule_request(self, data: dict, auth_key: str):

        data = json.dumps(data).encode("utf-8")
        future = self.publisher.publish(self.topic_path, data)
        # TODO error handler: https://cloud.google.com/pubsub/docs/publisher#publishing_messages
        return future
