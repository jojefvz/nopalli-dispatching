from dataclasses import dataclass

from ....common.command import Command


@dataclass
class CreateDispatch(Command):
    dispatch_ref: str
    containers: list[dict]
    stops: list[dict]