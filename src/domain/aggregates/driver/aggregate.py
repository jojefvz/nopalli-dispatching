from enum import Enum


class DriverStatus(Enum):
    AVAILABLE = 1
    WORKING = 2
    UNAVAILABLE = 3
    DEACTIVATED = 4

class Driver:
    def __init__(self, ref, name):
        self.reference = ref
        self.driver_status = DriverStatus.AVAILABLE
        self.name = name
        self.preassigned_dispatches = []
        self.dispatch_proposal = None

    def complete_task(self):
        pass
    def generate_answer(self):
        pass
