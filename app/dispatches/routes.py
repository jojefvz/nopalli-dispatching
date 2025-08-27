from flask import render_template, request, Response

from app.dispatches import bp
from src.domain.commands.dispatch import commands
from src.adapters.repository import DispatchRepository
from src.service_layer import messagebus, unit_of_work


@bp.route('/dispatches', methods=['GET'])
def dispatches_page():
    return render_template('dispatches/dispatches.html')

@bp.route('/', methods=['POST'])
def create_dispatch():
    cmd = commands.CreateDispatch(
        dispatch_ref=request.form['dispatch_ref'],
        containers=request.form['containers'],
        stops=request.form['stops']
    )

    uow = unit_of_work.SqlAlchemyUnitOfWork(DispatchRepository)
    messagebus.handle(cmd, uow)

    return Response(status=200)

