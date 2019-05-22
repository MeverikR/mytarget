from aiohttp import ClientSession

class Oauth():
    url = 'https://target-sandbox.my.com/api/v2/oauth2/token.json'
    async def oauth2(self,code,client_id):
        params = {
            "grant_type": "authorization_code",
            "code": str(code),
            "client_id": str(client_id)
        }
        async with ClientSession() as session:
            response = await session.post(self.url, data=params)
            data = await response.json()
            return data


    async def refresh(self, refresh_token,client_id,client_secret):
        headers = {
            "Content-Type" : "application/x-www-form-urlencoded"
        }
        params = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": client_id,
            "client_secret": client_secret
        }
        async with ClientSession() as session:
            response = await session.post(self.url, data=params, headers = headers)
            data = await response.json()
            return data
