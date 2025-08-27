from ....domain.aggregates.location.aggregate import Location, Address

def create_location(command, uow):
    with uow:
        uow.items.add(
            Location(
                name=command.name,
                address=Address(
                    street_address=command.street_address, 
                    city=command.city, 
                    state=command.state, 
                    zipcode=command.zipcode),
                )
            )
        
        uow.commit()