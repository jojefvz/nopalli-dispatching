
from ....domain.aggregates.dispatch.aggregate import Dispatch, Container
from ....domain.aggregates.dispatch.entities import Stop

        
def create_dispatch(command, uow):
    with uow:
        uow.dispatches.add(
            Dispatch(
                ref=command.dispatch_ref,
                containers=tuple([Container(number=c['number'], seal=c['seal'], weight=c['weight']) for c in command.containers]),
                stops=[Stop(priority=s['priority'], dispatch_ref=command.dispatch_ref) for s in command.stops]
                )
        )
        uow.commit()
