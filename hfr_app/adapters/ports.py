from abc import ABC, abstractmethod


class FeederCommunicationPort(ABC):

    @abstractmethod
    def publish_schedule_request(self, schedule_data: dict, auth_token: str):
        """
        Publish json like:
        {
        'id': schedule_id,
        'timestamp': '2020-09-14T14:14:00Z',
        'done': False,
        'feeder': feeder_id,
        'auth_token': hash_token
        }
        """
        pass
