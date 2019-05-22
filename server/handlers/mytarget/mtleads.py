from helpers.config import Config
from aiohttp import web
config = Config.get_config()
import logging


async def mtleads(request):
    logging.debug(request)
    app_id =  request.match_info.get('app')
    logging.debug('Подписан app_id: %s'%(app_id))

    return web.json_response({
        'data': True
    })


