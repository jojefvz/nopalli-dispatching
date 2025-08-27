from abc import ABC, abstractmethod


class DispatchRepository:
    def __init__(self, session):
        self.seen = set()
        self.session = session
        
    def add(self, dispatch):
        self.session.add(dispatch)
        self.seen.add(dispatch)


class BrokerRepository:
    def __init__(self, session):
        self.seen = set()
        self.session = session
        
    def add(self, broker):
        self.session.add(broker)
        self.seen.add(broker)


class LocationRepository:
    def __init__(self, session):
        self.seen = set()
        self.session = session
        
    def add(self, location):
        self.session.add(location)
        self.seen.add(location)