from sqlalchemy import ForeignKey, PickleType, Table, Column, Integer, String, create_engine, Enum
from sqlalchemy.orm import composite, registry, relationship

from ..domain.aggregates.broker.aggregate import Broker 
from ..domain.aggregates.dispatch.aggregate import Dispatch, DispatchStatus 
from ..domain.aggregates.dispatch.entities import Stop 
from ..domain.aggregates.location.aggregate import Address, Location 
from ..domain.aggregates.broker.aggregate import Broker 


mapper_registry = registry()

dispatch_table = Table(
    'dispatches',
    mapper_registry.metadata,
    Column('id', Integer, primary_key=True),
    Column('reference', String, unique=True),
    Column('status', Enum(DispatchStatus), nullable=False),
    Column('containers', PickleType),
)

stop_table = Table(
    'stops',
    mapper_registry.metadata,
    Column('id', Integer, primary_key=True),
    Column('dispatch_ref', ForeignKey('dispatches.reference')),
    Column('priority', Integer)
)

broker_table = Table(
    'brokers',
    mapper_registry.metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('street_address', String),
    Column('city', String),
    Column('state', String),
    Column('zipcode', Integer)
)

brokers_view = Table(
    'brokers_view',
    mapper_registry.metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('street_address', String),
    Column('city', String),
    Column('state', String),
    Column('zipcode', Integer)
)

location_table = Table(
    'locations',
    mapper_registry.metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('street_address', String),
    Column('city', String),
    Column('state', String),
    Column('zipcode', Integer)
)


def start_mappers():
    mapper_registry.map_imperatively(
        Dispatch,
        dispatch_table,
        properties={'stops': relationship(Stop, backref="stops", order_by=stop_table.c.priority)}
        )
    mapper_registry.map_imperatively(Stop, stop_table)

    mapper_registry.map_imperatively(
        Broker, 
        broker_table,
        properties={
            'address': composite(
                Address, 
                broker_table.c.street_address, 
                broker_table.c.city, 
                broker_table.c.state, 
                broker_table.c.zipcode)
                }
        )
    
    mapper_registry.map_imperatively(
        Location, 
        location_table,
        properties={
            'address': composite(
                Address, 
                location_table.c.street_address, 
                location_table.c.city, 
                location_table.c.state, 
                location_table.c.zipcode)
                }
        )
    


connection_str = 'postgresql+psycopg2://root:root@db:5432/nopalli'
engine = create_engine(connection_str)
mapper_registry.metadata.create_all(engine)


# from sqlalchemy import Table, Column, create_engine, String, Integer, Enum, select
# from sqlalchemy.orm import registry, Session
# from domain.dispatch import Dispatch, DispatchStatus, Container, ContainerList
