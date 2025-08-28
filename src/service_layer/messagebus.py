from typing import Union

from ..common import command, event
from ..domain.commands.broker import commands as broker_commands
from ..domain.commands.dispatch import commands as dispatch_commands
from ..domain.commands.location import commands as location_commands
from ..domain.events.broker import events
from .handlers.broker import handlers as broker_handlers
from .handlers.dispatch import handlers as dispatch_handlers
from .handlers.location import handlers as location_handlers


Message = Union[command.Command, event.Event]

def handle(message: Message, uow):
    results = []
    queue = [message]

    while queue:
        message = queue.pop(0)
        if isinstance(message, event.Event):
            print(f"CURRENT EVENT AT MESSAGE BUS: {message}")
            handle_event(message, queue, uow)
        elif isinstance(message, command.Command):
            print(f"CURRENT COMMAND AT MESSAGE BUS: {message}")
            cmd_result = handle_command(message, queue, uow)
            results.append(cmd_result)
        else:
            raise Exception(f'{message} was not an Event or Command')

    return results

def handle_event(event, queue, uow):
    for handler in EVENT_HANDLERS[type(event)]:
        try:
            handler(event, uow)
            queue.extend(uow.collect_new_events())
        except Exception:
            continue

def handle_command(command, queue, uow):
    try:
        handler = COMMAND_HANDLERS[type(command)]
        result = handler(command, uow)
        queue.extend(uow.collect_new_events())
        return result
    except Exception:
        raise


EVENT_HANDLERS = {
    events.BrokerCreated: [broker_handlers.add_broker_to_read_model],
}

COMMAND_HANDLERS = {
    location_commands.CreateLocation: location_handlers.create_location,
    broker_commands.CreateBroker: broker_handlers.create_broker,
    dispatch_commands.CreateDispatch: dispatch_handlers.create_dispatch,
}
