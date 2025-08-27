from enum import Enum
from dataclasses import dataclass

from ....common.entity import AggregateRoot
from ....common.value_object import ValueObject
from .entities import Stop, Instruction, Task


@dataclass
class Container(ValueObject):
    number: str
    seal: str
    weight: float

@dataclass
class StopSnapshot(ValueObject):
    location: str
    tasks: list[Task]

@dataclass
class DispatchProposal(ValueObject):
    reference: str
    containers: list[Container]
    stops: list[StopSnapshot]

class DispatchStatus(Enum):
    DRAFT = 1
    STARTED = 2
    POSTPONED = 3
    COMPLETED = 4
    CANCELLED = 5


MINIMUM_STOPS_REQUIRED = 2
MAXIMUM_STOPS_PERMITTED = 8
MAXIMUM_CONTAINERS_PER_DISPATCH = 4

class Dispatch(AggregateRoot):
    def __init__(self, ref, containers: list[Container], stops: list[Stop]):
        self.reference = ref
        self.status = DispatchStatus.DRAFT
        self.driver_ref = None
        self.containers = containers
        self.stops = stops
        self.events = []

    def associate_container_to_task(self, priority, task_priority, container):
        self.stops[priority - 1].tasks[task_priority].container_num = container.number

    def associate_container_to_all_tasks(self, container):
        for stop in self.stops:
            for task in stop.tasks:
                if task.instruction == Instruction.BOBTAIL_TO_NEXT_STOP:
                    continue
                task.container_num = container.number


    def append_stop(self, tasks):
        if self.status == DispatchStatus.COMPLETED:
            return 'Cannot add a stop when dispatch is completed.'
        
        if self.status == DispatchStatus.CANCELLED:
            return 'Cannot add a stop when dispatch is cancelled.'
        
        if len(self.stops) ==  MAXIMUM_STOPS_PERMITTED:
            return 'No more stops can be added, maximum limit reached.'
        
        self.stops.append(Stop(self.reference, tasks))
        
    def insert_stop(self, task):
        self.stops.insert(Stop(self.reference, task))

    def remove_stop(self, priority):
        if self.status == DispatchStatus.COMPLETED:
            return 'Cannot remove a stop when dispatch is completed.'
        
        if self.status == DispatchStatus.CANCELLED:
            return 'Cannot remove a stop when dispatch is cancelled.'
        
        if priority == 1 or priority == 2:
            return 'First two stops cannot be removed.'
        
        self.stops.pop(priority - 1)
        

    def generate_proposal(self):
        return DispatchProposal(
            self.reference,
            self.containers,
            
        )
