from dataclasses import dataclass

from ....common.command import Command


@dataclass
class CreateBroker(Command):
    name: str
    street_address: str
    city: str
    state: str
    zipcode: str


@dataclass
class UpdateBroker(Command):
    name: str
    street_address: str
    city: str
    state: str
    zipcode: str