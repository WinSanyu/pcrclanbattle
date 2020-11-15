import ujson
import aiohttp

from ghz.config import bot_key as key

async def aiohttprequest(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.text()

async def _from_api_get_json(url, key):
    url += key
    data_json_str = await aiohttprequest(url)
    data_json = ujson.loads(data_json_str)
    return data_json

async def get_data_from_bot():
    url = "https://pcr.stoodant.top/clan/600783086/statistics/api/?apikey="
    data = await _from_api_get_json(url, key)
    return data["challenges"]
    
async def get_member():
    url = "https://pcr.stoodant.top/clan/600783086/statistics/api/?apikey="
    _members = await _from_api_get_json(url, key)
    _members = _members["members"]
    members = {}
    for member in _members:
        members[member['qqid']] = member['nickname']
    return members