from logging import config as logger_config
from aiohttp import web
from helpers.config import Config
from helpers.cors import allow_cors
from handlers.main import Main
from handlers.mytarget import on_mytarget_response
from helpers.middlewares import auth_middleware
from handlers.mytarget.mtleads import mtleads



config = Config.get_config()

logger_config.dictConfig(config.get('logging'))

if __name__ == '__main__':
    app = web.Application(middlewares=[auth_middleware])
    app.router.add_route('GET', '/mytarget/', on_mytarget_response)
    app.router.add_route('POST','/mytarget/leads/{app}',mtleads)
    app.router.add_route('POST', '/', Main)
    allow_cors(app)

web.run_app(app, host=config.get('host'), port=config.get('port'))

