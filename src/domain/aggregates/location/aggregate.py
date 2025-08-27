from dataclasses import dataclass

from ....common.entity import AggregateRoot
from ....common.value_object import ValueObject


@dataclass
class Address(ValueObject):
    def __init__(self, street_address: str, city: str, state: str, zipcode: int):
        self.street_address = street_address
        self.city = city
        self.state = state
        self.zipcode = zipcode

class Location(AggregateRoot):
    def __init__(self, ref, name, address: Address):
        self.reference = ref
        self.name = name
        self.address = address
        self.events = []

