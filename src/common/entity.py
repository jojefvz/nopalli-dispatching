from uuid import uuid4

class Entity:
    def __init__(self):
        self.events = []

class AggregateRoot(Entity):
    pass