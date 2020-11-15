import copy

from ghz.process_data import get_challenges
from ghz.config import get_weights

def dict_sort(d):
    sorted_key_list = sorted(d, key = lambda x: d[x], reverse=True)
    sorted_dict = {}
    for key in sorted_key_list:
        sorted_dict[key] = d[key] 
    return sorted_dict    
    #  [{'nickname': '赤阳', 'damage': 557171, 'day': 5, 'is_continue': False, 'score': 557171}, {'nickname': '痛苦的魔皇', 'damage': 503375, 'day': 5, 'is_continue': False, 'score': 503375}]
def challenges_sort(d):
    sorted_key_list = sorted(d, key = lambda x: float(x['score']), reverse=True)
    return list(sorted_key_list)

async def weighted_score(challenges = None, weights = None, day = None, boss = None):
    if not weights:
        weights = await get_weights()    
    if not challenges:
        challenges = await get_challenges(weights = weights)    

    score = {}   
    for boss_id in challenges:
        if boss and boss != boss_id:
            continue
        for challenge in challenges[boss_id]:
            nickname = challenge['nickname']
            if nickname not in score:
                score[nickname] = 0
            if ((not day) or challenge['day'] in day):
                score[nickname] += challenge['score']
    return score
    
async def score2str(score=None, weights = None, day = None, boss = None, needsort = False):
    if not weights:
        weights = await get_weights()
    if not score:
        score = await weighted_score(weights = weights, day = day, boss = boss)
    res = ''
    if needsort:
        score = dict_sort(score)
        
        for i, nickname in enumerate(score):
            res += '\n{2}\t{1}\t{0}'.format(nickname, str(int(score[nickname])).zfill(8), str(i+1).zfill(2))
    else:        
        for nickname in score:
            res += '\n\t{1}\t{0}'.format(nickname, str(int(score[nickname])).zfill(8))
    return res
    
async def boss_info(boss = 'B5', reverse = False):
    res = {}
    weights = await get_weights()
    new_weights = copy.deepcopy(weights)
    new_weights[boss] = 1
    challenges = await get_challenges(weights = new_weights)
    bossinfo = challenges[boss]
    # for challenge in bossinfo:
        # if challenge['is_continue']:
            # continue
        # nickname = challenge['nickname']
        # if nickname not in res:
            # res[nickname] = []
        
        # res[nickname].append(float(challenge['score']))
    
    # avg = {}
    # for key in res:
        # avg[key] = sum(res[key])/len(res[key])
    bossinfo = challenges_sort(bossinfo)
    if reverse:
        bossinfo = bossinfo[::-1]
        
    res_str = ''
    cnt = 0
    for s in bossinfo:
        if s['is_continue']:
            continue
        cnt += 1
        res_str += '\n' + str(s['nickname']) + ': ' + str(s['score'])
        if cnt == 20:
            break
    return res_str
    # print(bossinfo)
    # return