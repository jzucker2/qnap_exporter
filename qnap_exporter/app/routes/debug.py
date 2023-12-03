from flask import current_app as app
from ..routers.debug_router import DebugRouter


log = app.logger


@app.route('/api/v1/qnap/debug')
def handle_debug_route():
    router = DebugRouter()
    return router.handle_debug_route_response()


@app.route('/api/v1/qnap/debug/pprint')
def handle_debug_pprint_route():
    router = DebugRouter()
    return router.handle_debug_pprint_route_response()


@app.route('/api/v1/qnap/debug/firmware/update')
def handle_debug_firmware_update_route():
    router = DebugRouter()
    return router.handle_debug_firmware_update_route_response()
