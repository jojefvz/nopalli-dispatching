from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DEFAULT_SESSION = sessionmaker(
    bind=create_engine('postgresql+psycopg2://root:root@db:5432/nopalli')
    )

class SqlAlchemyUnitOfWork:
    def __init__(self, session_factory=DEFAULT_SESSION):
        self.session_factory = session_factory
    
    def add_repo(self, repo):
        self.repo = repo
        
    def __enter__(self):
        self.session = self.session_factory()
        if self.repo:
            self.items = self.repo(self.session)

    def __exit__(self, *args):
        self.session.rollback()
        self.session.close()

    def collect_new_events(self):
        for item in self.items.seen:
            while item.events:
                yield item.events.pop(0)

    def commit(self):
        self.session.commit()
