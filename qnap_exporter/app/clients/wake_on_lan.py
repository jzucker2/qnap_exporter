import asyncio
from flask import current_app as app


log = app.logger


class WakeOnLanException(Exception):
    pass


class WakeOnLanHostDownException(WakeOnLanException):
    pass


class WakeOnLanTimeoutException(WakeOnLanException):
    pass


class WakeOnLan(object):
    @classmethod
    def get_client(cls):
        return cls()

    @classmethod
    async def wake_up(cls,
                      mac_address,
                      ip_address,
                      delay_after_wake=0):
        log.info(f'!!!!!!!!! try sending magic packet to mac_address'
                 f' ({mac_address}) at ip: {ip_address} !!!!!!!!! ')
        await asyncio.sleep(0)
