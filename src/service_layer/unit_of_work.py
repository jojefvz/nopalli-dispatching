from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..adapters.repository import BrokerRepository

DEFAULT_SESSION = sessionmaker(
    bind=create_engine('postgresql+psycopg2://root:root@db:5432/nopalli')
    )

class BrokerUnitOfWork:
    def __init__(self, session_factory=DEFAULT_SESSION):
        self.session_factory = session_factory
        
    def __enter__(self):
        self.session = self.session_factory()
        self.brokers = BrokerRepository(self.session)
        return self

    def __exit__(self, *args):
        self.session.rollback()
        self.session.close()

    def collect_new_events(self):
        for broker in self.brokers.seen:
            while broker.events:
                yield broker.events.pop(0)

    def commit(self):
        self.session.commit()
        
