import re, jwt
from aiohttp import web
from helpers.config import Config


config = Config.get_config()



JWT_EXP_DELTA_SECONDS =int(config.get('security').get('jwt_expire_seconds'))
JWT_SECRET = str(config.get('security').get('jwt_secret'))
JWT_ALGORITHM = str(config.get('security').get('jwt_algorithm'))

WHITE_LIST_ROUTES = [r'/login', r'/check_health',r'/add_user/posts',r'/add_user/posts',r'/add_user/posts/{id}',r'/',r'/vkleads/{hash}',r'/vkleads/',r'/vkleads',r'/api/']

def check_request(request, entries):
    """
    Метод проверки маршрута, нужен для авторизации
    :param request:
    :param entries:
    :return:
    """
    for pattern in entries:
        if re.match(pattern, request.path):
            return True

    return False


@web.middleware
async def auth_middleware(request, handler):
    """
    Проверяем токен в каждом запросе
    :param request:
    :param handler:
    :return:
    """
    # в каждый реквест будем добавлять поле auth

    request.auth = None
    if check_request(request, WHITE_LIST_ROUTES): # если белый роут, пропускаем без токена
        return await handler(request)
    if request.method == 'OPTIONS':
        return await handler(request)


    # дергаем из заголовка авторизацию
    if 'Authorization' not in request.headers:
        raise web.HTTPForbidden(
            reason='Please login first',
        )


    try:
        scheme, jwt_token = request.headers.get(
            'Authorization'
        ).strip().split(' ')
    except ValueError:
        raise web.HTTPForbidden(
            reason='Please login first',
        )


    if not jwt_token:
        msg = 'Please login!'
        return web.HTTPUnauthorized(reason=msg , body=msg )

    try:
        jwt_token = jwt_token.strip('"').strip("'")
        # так как подделать payload не могут, вся инфа у нас уже будет внутри, в БД за данными юзера ходить не надо
        request.auth = jwt.decode(jwt_token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.DecodeError:
        msg = 'Security problem. Please, relogin!'
        return web.HTTPUnauthorized(reason=msg, body=msg)

    except jwt.ExpiredSignatureError:
        msg = 'Security problem. Your session has expired. Please login!'
        return web.HTTPUnauthorized(reason=msg, body=msg)
    except Exception as e:
        return web.HTTPBadRequest(reason=str(e), body=str(e))
    return await handler(request)
