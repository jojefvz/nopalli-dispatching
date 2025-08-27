from sqlalchemy import text
from ..service_layer import unit_of_work


def brokers(uow: unit_of_work.SqlAlchemyUnitOfWork):
    results = uow.session.execute(text(
        """
        SELECT * FROM brokers_view
        """
        )     
    ).all()

    print(results)
    return results