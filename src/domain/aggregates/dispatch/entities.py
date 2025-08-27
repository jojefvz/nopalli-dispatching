from dataclasses import dataclass, field
from datetime import date, time
from enum import Enum
from typing import Optional

from ....common.entity import Entity
from ....common.value_object import ValueObject


class Instruction(Enum):
    PREPULL_CONTAINER = 'prepull_container'
    BOBTAIL_TO_NEXT_STOP = 'bobtail_to_next_stop'
    PICKUP_EMPTY_CONTAINER = 'pickup_empty_container'
    DROP_EMPTY_CONTAINER = 'drop_empty_container'
    LIVE_LOAD_CONTAINER = 'live_load_container'
    PICKUP_LOADED_CONTAINER = 'pickup_loaded_container'
    DROP_LOADED_CONTAINER = 'drop_loaded_container'
    LIVE_UNLOAD_CONTAINER = 'live_unload_container'
    TERMINATE_CONTAINER = 'terminate_container'
    INGATE_CONTAINER = 'ingate_container'
    YARD_PULL_CONTAINER = 'yard_pull_container'
    STREET_TURN_CONTAINER = 'street_turn_container'

class AppointmentTimeType(Enum):
    OPEN_APPOINTMENT = 'open_appointment'
    EXACT_TIME_APPOINTMENT = 'exact_time_appointment'
    TIME_WINDOW_APPOINTMENT = 'time_window_appointment'
    READY_AFTER_APPOINTMENT = 'ready_after_appointment'
    DO_BEFORE_APPOINTMENT = 'do_before_appointment'

@dataclass
class AppointmentTime(ValueObject):
    appointment_type: AppointmentTimeType = None
    start_time: time = None
    end_time: time = None

@dataclass
class Task(ValueObject):
    instruction: Instruction
    container_num: str = None
    completed: bool = False
    appointment_time: AppointmentTime = field(default_factory=AppointmentTime)

MINIMUM_TASKS_REQUIRED = 1
MAXIMUM_TASKS_PERMITTED = 3

class Stop(Entity):
    def __init__(self, location_ref: str, dispatch_ref: str, appointment_date: Optional[date], tasks: list[Task]):
        self.location_ref = location_ref
        self.dispatch_ref = dispatch_ref
        appointment_date = appointment_date
        self.tasks = tasks

    def add_task(self, instruction):
        if len(self.tasks) == MAXIMUM_TASKS_PERMITTED:
            return "No more tasks can be added"
        if not self._can_add_task(instruction):
            return "Instruction incompatible with previous task"
            
        self.tasks.append(Task(instruction))
            
    def _can_add_task(self, instruction):
        if self.tasks[0].instruction in (Instruction.PICKUP_EMPTY_CONTAINER, Instruction.PICKUP_LOADED_CONTAINER):
            return False
        if self.tasks[0].instruction in (Instruction.DROP_EMPTY_CONTAINER, Instruction.DROP_LOADED_CONTAINER) \
            and instruction in (Instruction.DROP_EMPTY_CONTAINER, Instruction.DROP_LOADED_CONTAINER):
            return False
        if self.tasks[0].instruction == Instruction.BOBTAIL_TO_NEXT_STOP \
            and instruction in (Instruction.DROP_EMPTY_CONTAINER, Instruction.DROP_LOADED_CONTAINER, Instruction.BOBTAIL_TO_NEXT_STOP,
                                Instruction.PICKUP_EMPTY_CONTAINER, Instruction.PICKUP_LOADED_CONTAINER, Instruction.LIVE_UNLOAD_CONTAINER,
                                Instruction.LIVE_LOAD_CONTAINER):
            return False
        if self.tasks[0].instruction == Instruction.TERMINATE_CONTAINER \
            and instruction == Instruction.TERMINATE_CONTAINER:
            return False
        
        return True
        
    def remove_task(self, task_priority):
        if len(self.tasks) == MINIMUM_TASKS_REQUIRED:
            return 'Cannot have less than one task.'
        
        self.tasks.pop(task_priority - 1)
