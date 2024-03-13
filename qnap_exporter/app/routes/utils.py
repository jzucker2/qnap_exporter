from flask import current_app as app
from ..utils import get_version


log = app.logger


# Keep this simple for debugging
# and to reduce imports here
@app.route('/hey')
@app.route('/api/v1/hey')
@app.route('/utils/hey')
def hey():
    log.debug('hey route')
    return {'message': 'in a bottle'}


@app.route('/health')
@app.route('/api/v1/health')
@app.route('/utils/health')
def health():
    log.debug('health check')
    return {
        'message': 'healthy',
        'version': get_version(),
    }


@app.route('/utils/version')
def version():
    return {
        # FIXME: replace with a constant
        'server': 'qnap_exporter',
        'version': get_version(),
    }
