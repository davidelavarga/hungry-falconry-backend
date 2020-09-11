from abc import ABC, abstractmethod


class FeederCommunicationPort(ABC):

    @abstractmethod
    def publish_schedule_request(self):
        pass
