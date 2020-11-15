import ujson
import aiofiles
bot_key = "meB6SQhNuXgy5kj9"

async def get_weights():
    filename = 'ghz/weights.json'
    async with aiofiles.open(filename, mode='r') as f:
        f = await f.read()
    f = open(filename, 'r')
    weights = ujson.load(f)
    true_weights = {}
    for key in weights:
        true_weights[key] = 100 / weights[key]
    return true_weights

#---------------------------------------------------------------------------------------------------#    

async def print_weights(weights = None):
    if not weights:
        weights = await get_weights()
    str_weight = '权重: '
    for boss_id in weights:
        str_weight += '\n\t{0:4s} {1}'.format(boss_id, round(weights[boss_id], 2))
    return str_weight