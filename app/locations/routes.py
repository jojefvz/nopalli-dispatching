from flask import render_template, request, redirect

from app.locations import bp
from src.adapters.repository import LocationRepository
from src.domain.commands.location import commands
from src.service_layer import unit_of_work, messagebus


@bp.route('/locations', methods=['GET'])
def locations_page():
    return render_template('locations/locations.html')


@bp.route('/dispatches', methods=['POST'])
def create_location():
    cmd = commands.CreateLocation(
        name=request.form['name'],
        street_address=request.form['street_address'],
        city=request.form['city'],
        state=request.form['state'],
        zipcode=request.form['zipcode']
    )

    uow = unit_of_work.SqlAlchemyUnitOfWork(LocationRepository)
    messagebus.handle(cmd, uow)

    return redirect('dispatches.html')