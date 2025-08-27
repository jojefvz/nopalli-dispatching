from flask import redirect, render_template, request, url_for

from app.brokers import bp
from src.adapters.repository import BrokerRepository
from src.domain.commands.broker import commands
from src.service_layer import messagebus, unit_of_work
from src.views import brokers_view


@bp.route('/brokers', methods=['GET'])
def brokers_page():
    uow = unit_of_work.SqlAlchemyUnitOfWork()
    brokers = brokers_view.brokers(uow)
    return render_template('brokers/brokers.html', brokers=brokers)


@bp.route('/brokers', methods=['POST'])
def create_broker():
    cmd = commands.CreateBroker(
        name=request.form['name'],
        street_address=request.form['street_address'],
        city=request.form['city'],
        state=request.form['state'],
        zipcode=request.form['zipcode']
    )

    uow = unit_of_work.SqlAlchemyUnitOfWork()
    uow.repo = BrokerRepository
    messagebus.handle(cmd, uow)

    return redirect(url_for('brokers.brokers_page'))

@bp.route('/brokers', methods=['GET'])
def get_broker():
    cmd = commands.GetBroker()
    return render_template()

@bp.route('/brokers', methods=['POST'])
def update_broker():
    cmd = commands.UpdateBroker(
        name=request.form['name'],
        street_address=request.form['street_address'],
        city=request.form['city'],
        state=request.form['state'],
        zipcode=request.form['zipcode']
    )
