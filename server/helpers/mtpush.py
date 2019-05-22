import aiohttp


class pushMT():

    url = 'https://target-sandbox.my.com/api/v2/subscriptions.json'
    async def push(self, token,app_id):
        params ={
            'resource': 'OKLEADAD',
            'callback_url': 'url' +str(app_id)
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + str(token)
        }
        print(params)
        print(headers)
        import json
        async with aiohttp.ClientSession() as session:
            response = await session.post(self.url, data=json.dumps(params), headers=headers)
            data = await response.json()
            return data



    async def statistics(self,token,date_from,date_to,app_id):
        url = 'https://target-sandbox.my.com/api/v2/statistics/campaigns/day.json'
        headers = {"Authorization": "Bearer " + str(token)}
        params = {
            "date_from": date_from,
            "date_to": date_to,
            "id": app_id
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, headers= headers) as resp:
                data = await resp.json()
        return data







