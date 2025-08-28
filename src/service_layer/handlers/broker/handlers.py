from sqlalchemy import text

from ....domain.aggregates.broker.aggregate import broker_factory
from ....domain.commands.broker.commands import CreateBroker
from ....domain.events.broker.events import BrokerCreated


def create_broker(command: CreateBroker, uow):
    with uow:
        broker = broker_factory(
            command.name,
            command.street_address,
            command.city,
            command.state,
            command.zipcode
        )
        
        uow.brokers.add(broker)
        uow.commit()

def add_broker_to_read_model(event: BrokerCreated, uow):
    with uow:
        print("HERE BEFORE THE INSERT")
        uow.session.execute(text(
                """INSERT INTO brokers_view (name, street_address, city, state, zipcode)
                VALUES (:name, :street_address, :city, :state, :zipcode)"""),
                dict(
                    name=event.name,
                    street_address=event.street_address,
                    city=event.city,
                    state=event.state,
                    zipcode=event.zipcode
                    )
            )

        print("HERE AFTER THE INSERT")
        uow.commit()
