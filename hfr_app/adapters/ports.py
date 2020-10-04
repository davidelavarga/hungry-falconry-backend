from abc import ABC, abstractmethod


class FeederCommunicationPort(ABC):

    @abstractmethod
    def publish_schedule_request(self, data: dict, auth_key: str):
        pass


class SecretsStorePort(ABC):

    @abstractmethod
    def get_database_password(self, secret_id: str):
        pass
