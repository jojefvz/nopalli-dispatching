from dataclasses import dataclass

from ....common.event import Event

@dataclass
class BrokerCreated(Event):
    name: str
    street_address: str
    city: str
    state: str
    zipcode: int