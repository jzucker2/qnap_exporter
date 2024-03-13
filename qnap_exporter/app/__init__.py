# based around https://github.com/jzucker2/filmstock
from flask import Flask
from . import config
from .extensions import cors, scheduler
from .metrics import metrics


def create_app(config=config.base_config):
    """Returns an initialized Flask application."""
    app = Flask(__name__)
    app.config.from_object(config)

    with app.app_context():
        # TODO: make this based from `config`

        log_level = app.config.get('QNAP_EXPORTER_LOGGING_LEVEL')
        app.logger.setLevel(log_level)
        app.logger.debug(f'!!!!!!!!!!! Set log_level: {log_level}')

        # Check to possibly include our Tasks
        from .tasks.qnap_pinger import QNAPPinger
        if QNAPPinger.should_schedule_qnap_metrics_updates():
            from .tasks import qnap  # noqa: F401
        else:
            s_m = 'Skipping scheduling of QNAP metrics updates'
            app.logger.warning(s_m)

        register_extensions(app)

        @app.route("/")
        def hello_world():
            # FIXME: replace with a constant
            return "<p>Welcome to QNAP Exporter!</p>"

        # Include our Routes
        from .routes import utils  # noqa: F401
        from .routes import debug  # noqa: F401
        from .routes import collector  # noqa: F401

        # after routes, register metrics
        register_metrics(app)

    return app


def register_extensions(app):
    """Register extensions with the Flask application."""
    cors(app)
    # scheduler
    scheduler.init_app(app)
    scheduler.start()
    app.logger.debug('done registering extensions')


def register_metrics(app):
    metrics.init_app(app)


# def register_errorhandlers(app):
#     """Register error handlers with the Flask application."""
#
#     def render_error(e):
#         return render_template('errors/%s.html' % e.code), e.code
#
#     for e in [
#         requests.codes.INTERNAL_SERVER_ERROR,
#         requests.codes.NOT_FOUND,
#         requests.codes.UNAUTHORIZED,
#     ]:
#         app.errorhandler(e)(render_error)
