import asyncio
import logging
from datetime import datetime,timedelta
from logging import config as logger_config
from helpers.oauth import Oauth
from helpers.mtpush import pushMT
from helpers.config import Config
import aiocron
import asyncpg
import config
oauth = Oauth()

config = Config.get_config()
stat = pushMT()

logger_config.dictConfig(config.get('logging'))


@aiocron.crontab('0 0 * * *')
@asyncio.coroutine
async def attime_refresh():
    date_to = datetime.now().strftime("%d.%m.%Y")
    date_from = (datetime.now() + timedelta(days=-1)).strftime("%d.%m.%Y")

    conn = await asyncpg.connect(**config['db'])

    refresh = await conn.fetch('''
               SELECT refresh_token,app_id
               FROM data_user where refresh_token IS not NULL 
               ''')
    for data in refresh:
        refresh_token = data['refresh_token']
        data_refresh = await oauth.refresh(refresh_token, config['mytarget']['client_id'],config['mytarget']['client_secret'])
        logging.debug(data_refresh)

        update_token = await conn.execute('''UPDATE data_user
                    SET access_token = '%s',
                        refresh_token = '%s'
                      WHERE refresh_token = '%s'

                    ''' % (data_refresh['access_token'], data_refresh['refresh_token'], data['refresh_token']))
        static = await stat.statistics(data_refresh['access_token'], date_from, date_to, data['app_id'])
        logging.debug(static)
    await conn.close()



asyncio.get_event_loop().run_forever()
