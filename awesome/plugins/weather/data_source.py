import aiohttp
import ujson

async def aiohttprequest(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.text()

async def get_HeWeather(city):
    url = 'https://free-api.heweather.net/s6/weather/now?location={}&key=55fdb1a6f66041009440572df8bbf636'.format(city)
    r = await aiohttprequest(url)
    d = ujson.loads(r)
    d = d['HeWeather6'][0]
    info = d['update']['utc']
    d = d['now']
    info += '\n' + city + d['cond_txt']
    info += '\n温度 {}℃'.format(d['fl'])
    info += '\n相对湿度 {}'.format(d['hum'])
    return info

async def get_weather_of_city(city: str) -> str:
    # 这里简单返回一个字符串
    # 实际应用中，这里应该调用返回真实数据的天气 API，并拼接成天气预报内容
    return await get_HeWeather(city)