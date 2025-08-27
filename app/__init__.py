from flask import Flask

from src.adapters import orm


def create_app():
    app = Flask(__name__)
    orm.start_mappers()


    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.dispatches import bp as dispatches_bp
    app.register_blueprint(dispatches_bp)

    from app.brokers import bp as brokers_bp
    app.register_blueprint(brokers_bp)

    from app.locations import bp as locations_bp
    app.register_blueprint(locations_bp)

    return app