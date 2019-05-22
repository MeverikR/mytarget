import asyncpg
from helpers.config import Config
from helpers.oauth import Oauth
from helpers.mtpush import pushMT
from aiohttp import web
config = Config.get_config()
oauth = Oauth()
push = pushMT()
import logging

async def on_mytarget_response (request):
    logging.debug(request)
    result = request.rel_url.query
    if not result:
        return web.json_response({
            "status" : False
        })
    else:
        app_id = result['state']

        data = await oauth.oauth2(result['code'], config['mytarget']['client_id'])
        logging.debug(data)
        if 'error_description' in data:
            return web.json_response(data)
        else:
            conn = await asyncpg.connect(**config['db'])
            await conn.execute('''
                            INSERT INTO data_user (app_id,access_token, token_type, expires_in, refresh_token, tokens_left,social) 
                            VALUES('%s','%s','%s','%s','%s','%s','mytarget')
                            ''' % (
                app_id, data['access_token'], data['token_type'], data['expires_in'], data['refresh_token'],
                data['tokens_left']))

            subscription = await push.push(data['access_token'],app_id)
            logging.debug(subscription)
            await conn.close()
            return web.json_response({
                "status": True
            })








