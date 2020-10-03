import os
import json
from hfr_app.adapters.ports import FeederCommunicationPort, SecretsStorePort
from google.cloud import pubsub_v1  # TODO Use Pub/Sub Lite instead Pub/Sub
from google.cloud import secretmanager

GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
PROJECT_ID = os.getenv("PROJECT_ID")
TOPIC_ID = os.getenv("TOPIC_ID")


class GooglePubSubAdapter(FeederCommunicationPort):

    def __init__(self):
        self.publisher = pubsub_v1.PublisherClient()
        self.topic_path = self.publisher.topic_path(PROJECT_ID, TOPIC_ID)

    def publish_schedule_request(self, data: dict, auth_key: str):
        data = json.dumps(data).encode("utf-8")
        # auth_key will be used in order to difference the subscriber
        future = self.publisher.publish(self.topic_path, data, auth_key=auth_key)
        # TODO error handler: https://cloud.google.com/pubsub/docs/publisher#publishing_messages
        print(future.result())
        return future


def create_topic():
    """Create a new Pub/Sub topic."""

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)

    topic = publisher.create_topic(request={"name": topic_path})

    print("Topic created: {}".format(topic))


class GoogleSecretManager(SecretsStorePort):

    def __init__(self):
        self.secret_manager = secretmanager.SecretManagerServiceClient()

    def get_database_password(self, secret_id):
        response = self.secret_manager.access_secret_version(request={"name": self.__build_secret_resource(secret_id)})
        return response.payload.data.decode("UTF-8")

    @staticmethod
    def __build_secret_resource(secret_id, version_id="latest"):
        return f"projects/{PROJECT_ID}/secrets/{secret_id}/versions/{version_id}"
