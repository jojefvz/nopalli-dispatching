from src.domain.aggregates.broker.aggregate import Broker
from src.domain.aggregates.dispatch.aggregate import Dispatch
from src.domain.aggregates.location.aggregate import Location
    

class BrokerRepository:
    def __init__(self, session):
        self.seen = set()
        self.session = session
        
    def add(self, broker: Broker):
        self.session.add(broker)
        self.seen.add(broker)


class DispatchRepository:
    def __init__(self, session):
        self.seen = set()
        self.session = session
        
    def add(self, dispatch: Dispatch):
        self.session.add(dispatch)
        self.seen.add(dispatch)


class LocationRepository:
    def __init__(self, session):
        self.seen = set()
        self.session = session
        
    def add(self, location: Location):
        self.session.add(location)
        self.seen.add(location)
