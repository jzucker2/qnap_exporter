from flask import current_app as app
from ..routers.magic_router import MagicRouter


log = app.logger


@app.route('/api/v1/magic/packet', methods=['POST'])
async def send_magic_packet():
    router = MagicRouter()
    return await router.send_magic_packet_response()
