from dataclasses import dataclass

from ....common.command import Command


@dataclass
class CreateLocation(Command):
    name: str
    street_address: str
    city: str
    state: str
    zipcode: str