from sqlalchemy import text


def all_brokers(uow):
    with uow:
        results = uow.session.execute(text(
            """
            SELECT * FROM brokers_view
            """
            )     
        ).all()

        print(f"RESULTS FROM BROKER VIEW: {results}")
        return results