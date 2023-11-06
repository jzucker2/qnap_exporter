import asyncio
from flask import current_app as app
from requests.exceptions import ConnectTimeout
from wakeonlan import send_magic_packet


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
        try:
            response = send_magic_packet(mac_address,
                                         ip_address=ip_address)
            log.info(f'wake on lan got response: {response}')
        except ConnectTimeout as t:
            raise WakeOnLanTimeoutException(f'Timeout! with {t}') from t
        except OSError as o:
            raise WakeOnLanHostDownException(f'Host is down: {o}') from o
        except Exception as e:
            raise WakeOnLanException(f'Got other exception: {e}') from e
        log.info('!!!!!!!!! sent magic packet !!!!!!!!!')
        if delay_after_wake:
            log.info(f'!!!!!!!!! after wake on lan, wait ...'
                     f' {delay_after_wake} !!!!!!!!!')
            # if get power too quickly we flip off tv
            # therefore, we pause
            await asyncio.sleep(delay_after_wake)
