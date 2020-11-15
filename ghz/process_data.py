from ghz.data import get_member
from ghz.config import get_weights
from ghz.data import get_data_from_bot

def _get_boss(challenge):
    if challenge['cycle'] == 1:
        return 'A{}'.format(challenge['boss_num'])
    elif challenge['cycle'] == 2:
        return 'B{}'.format(challenge['boss_num'])
    elif challenge['cycle'] == 3:
        return 'C{}'.format(challenge['boss_num'])        

def _get_day(challenge, challenges):
    '''
    返回值k: 
        会战的第k天, 1 <= k <= 6
    '''
    return (challenge['challenge_pcrdate'] - challenges[0]['challenge_pcrdate']) + 1 

def _preprocess(challenges):
    '''
    目前仅用于判断是否尾刀，是的话也令is_continue为True
    '''
    for i, challenge in enumerate(challenges):
        if challenge['is_continue']:
            for j in range(i - 1, -1, -1):
                if challenges[j]['qqid'] == challenge['qqid']:
                    challenges[j]['is_continue'] = True
                    break

async def add_weighted(challenges, weights = None):
    '''
    用于算分，使得challenge获得属性score
    '''
    if not weights:
        weights = await get_weights()
    for boss_id in challenges:
        weight = weights[boss_id]
        for challenge in challenges[boss_id]:
            challenge['score'] = challenge['damage']*weight
    
async def processing_challenges(challenges_from_bot=None, day_first=1, day_end=5):
    r"""Return the current weighted scores
    
    Arguments:
        challenges: Use with get_data_from_bot()
        day_first: The first day need to use
        day_end: The last day need to use

    Returns:
        {
            'A1': [challenge1, challenge2, ...],
            'A2': [challenge1, challenge2, ...], 
            ...
            'B5': [challenge1, challenge2, ...]
        }
        where challenge_i = {'damage': int, 'day': int, 'is_continue': bool}
    """
    if not challenges_from_bot:
        challenges = await get_data_from_bot()
    else:
        challenges = challenges_from_bot
        
    _preprocess(challenges)    
    
    try:
        members = await get_member()
    except:
        members = {}
    
    res_challenges = {
        'A1': [], 
        'A2': [], 
        'A3': [],  
        'A4': [], 
        'A5': [], 
        'B1': [], 
        'B2': [], 
        'B3': [], 
        'B4': [], 
        'B5': [], 
        'C1': [], 
        'C2': [], 
        'C3': [], 
        'C4': [], 
        'C5': [], 
        }
    for i, challenge in enumerate(challenges):
        boss = _get_boss(challenge)
        res_challenge = {}
        tmp = {}
        
        if int(challenge['qqid']) not in members:
            tmp['nickname'] = 'qq' + str(challenge['qqid'])
        else:
            tmp['nickname'] = members[challenge['qqid']]
            
        tmp['damage'] = challenge['damage']
        tmp['day'] = _get_day(challenge, challenges)
        tmp['is_continue'] = False
        
        if challenge['is_continue']:
            tmp['is_continue'] = True

        res_challenges[boss].append(tmp)
    return res_challenges

async def get_challenges(challenges_from_bot=None, weights = None):
    r"""按boss返回处理后的bot数据
    example:
        res['A1'] = [{'nickname': u1dbq,  'damage': 114514, 'day': 1, 'is_continue': False, 'score': 114514.0}, ...]
    """
    if not weights:
        weights = await get_weights()
    if not challenges_from_bot:
        challenges = await processing_challenges()
    else:
        challenges = challenges_from_bot
    await add_weighted(challenges, weights)
    
    return challenges
            
if __name__ == '__main__':    
    challenges = get_data_from_bot()
    challenges = get_challenges(challenges)
    print(dict_sort(weighted_score(challenges)))    