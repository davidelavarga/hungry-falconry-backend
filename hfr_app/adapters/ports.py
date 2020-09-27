from abc import ABC, abstractmethod


class FeederCommunicationPort(ABC):

    @abstractmethod
    def publish_schedule_request(self, data: dict, auth_key: str):
        pass
