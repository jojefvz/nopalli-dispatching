from sqlalchemy import text

from ....domain.aggregates.broker.aggregate import broker_factory
from ....domain.commands.broker.commands import CreateBroker, UpdateBroker
from ....domain.events.broker.events import BrokerCreated
from ....domain.services import Dispatcher
from ...unit_of_work import SqlAlchemyUnitOfWork


def create_broker(command: CreateBroker, uow):
    with uow:
        broker = broker_factory(
            command.name,
            command.street_address,
            command.city,
            command.state,
            command.zipcode
        )
        
        uow.items.add(broker)
        uow.commit()

def add_broker_to_read_model(event: BrokerCreated, uow: SqlAlchemyUnitOfWork):
    print("HERE AT READ MODEL")
    with uow:
        print("HERE BEFORE THE INSERT")
        uow.session.execute(text(
                """INSERT INTO brokers_view (name, street_address, city, state, zipcode)
                VALUES (:name, :street_address, :city, :state, :zipcode)"""),
                dict(name=event.name, street_address=event.street_address, city=event.city, state=event.state, zipcode=event.zipcode)
            )

        print("HERE AFTER THE INSERT")
        uow.commit()

# def get_broker():


# def update_broker(command: UpdateBroker, uow):
#     with uow:
#         uow.repo.get()