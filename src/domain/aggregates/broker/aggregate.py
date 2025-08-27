from ...events.broker import events
from ....common.entity import AggregateRoot
from ..location.aggregate import Address


class Broker(AggregateRoot):
    def __init__(self, name: str, address: Address):
        self.name = name
        self.address = address
        self.events = []
        
def broker_factory(name: str, street_address: str, city: str, state: str, zipcode: str):
    broker = Broker(
        name,
        Address(
            street_address,
            city,
            state,
            int(zipcode)
        )
    )
    
    broker.events.append(events.BrokerCreated(
        broker.name,
        broker.address.street_address,
        broker.address.city,
        broker.address.state,
        broker.address.zipcode
    ))

    return broker
