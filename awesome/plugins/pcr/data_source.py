from ghz.config import print_weights
from ghz.analize import score2str, boss_info

async def get_weights() -> str:
    return await print_weights()
    
async def get_score(day = None) -> str:
    if day:
        res = '第 {} 天的得分'.format(day).replace('{', '').replace('}', '')
    else:
        res = '得分'
    score = await score2str(day = day)
    if score:
        return res + score
    else:
        return res + '\n\t好像没有数据的样子'
        
async def get_rank(day = None) -> str:
    if day:
        res = '第 {} 天的排名'.format(day).replace('{', '').replace('}', '')
    else:
        res = '排名'
    score = await score2str(day = day, needsort=True)
    if score:
        return res + score
    else:
        return res + '\n\t好像没有数据的样子'        
    
async def get_boss_info(boss_id, reverse = False) -> str:
    res = boss_id + '伤害'
    score = await boss_info(boss_id, reverse)
    if score:
        return res + score
    else:
        return res + '\n\t好像没有数据的样子'   
    
# async def strs2str(strs):
    
    # return res
        
