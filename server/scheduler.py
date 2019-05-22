import asyncio
import logging
from logging import config as logger_config
from time import gmtime, strftime
from datetime import datetime, timedelta
import json
from helpers.config import Config
import aiocron
import asyncpg
import config
from helpers.call_api import CallApi

config = Config.get_config()

logger_config.dictConfig(config.get('logging'))

call_api = CallApi()
time = strftime("%H:%M:%S", gmtime())


@aiocron.crontab('* * * * *')
@asyncio.coroutine
async def attime():
    conn = await asyncpg.connect(**config['db'])
    recalls = await conn.fetch('''
               SELECT data_user.work_start,data_user.token,data_user.vnumber_call,data_user.scenario_id,data_user.method,recall.form_id,recall.visitor_phone_number,recall.id,recall.status
               FROM recall
               LEFT JOIN data_user ON recall.ids = data_user.id
                where  cast(date_time as timestamp)<= '%s'
            ''' % (datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")))
    for event_call in recalls:
        if not event_call['status']:
            if event_call.get('scenario_id') != '':
                scenario_id = int(event_call.get('scenario_id'))
            else:
                scenario_id = event_call.get('scenario_id')
            calls = await call_api.call(event_call['method'],event_call['token'], event_call['vnumber_call'],
                                        event_call['visitor_phone_number'],
                                       scenario_id)

            calls_status = await conn.execute('''UPDATE recall
            SET status = '%s' WHERE id = '%s'
            ''' % (json.dumps(calls), event_call['id']))
            logging.debug(calls)

    await conn.close()

asyncio.get_event_loop().run_forever()
