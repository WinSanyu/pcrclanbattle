import re

from nonebot import on_command, CommandSession
import nonebot.permission as perm

from .data_source import get_weights, get_score, get_rank, get_boss_info

@on_command('weights', aliases=('weight', '权重'), only_to_me = False, permission = perm.GROUP)
async def score(session: CommandSession):
    weights_str = await get_weights()
    await session.send(weights_str)

# @on_command('debug')
# async def debug(session: CommandSession):
    # message = await get_debug_message()
    # await session.send(message)
    # q = session.ctx['user_id']
    # await session.send(f'[CQ:at,qq={q}]')
    
@on_command('score', aliases=('得分', '加权得分', '分数', '加权分数'), only_to_me = False)
async def score(session: CommandSession):
    day = session.get('day_for_score')
    score_str = await get_score(day = day)
    await session.send(score_str)
    
    
@on_command('排名', only_to_me = False, permission = perm.GROUP_ADMIN)
async def rank(session: CommandSession):
    day = session.get('day_for_rank')
    score_str = await get_rank(day = day)
    await session.send(score_str)
    
@on_command('1王伤害', aliases=('一王伤害'), only_to_me = False, permission = perm.GROUP_ADMIN)
async def boss1_rank(session: CommandSession):
    score_str = await get_boss_info('B1')
    await session.send(score_str)
    score_str = await get_boss_info('B1', reverse = True)
    await session.send(score_str)

@on_command('2王伤害', aliases=('二王伤害'), only_to_me = False, permission = perm.GROUP_ADMIN)
async def boss2_rank(session: CommandSession):
    score_str = await get_boss_info('B2')
    await session.send(score_str)   
    score_str = await get_boss_info('B2', reverse = True)
    await session.send(score_str)    
    
@on_command('3王伤害', aliases=('三王伤害'), only_to_me = False, permission = perm.GROUP_ADMIN)
async def boss3_rank(session: CommandSession):
    score_str = await get_boss_info('B3')
    await session.send(score_str)   
    score_str = await get_boss_info('B3', reverse = True)
    await session.send(score_str)    

@on_command('4王伤害', aliases=('四王伤害'), only_to_me = False, permission = perm.GROUP_ADMIN)
async def boss4_rank(session: CommandSession):
    score_str = await get_boss_info('B4')
    await session.send(score_str)   
    score_str = await get_boss_info('B4', reverse = True)
    await session.send(score_str)        
    
@on_command('5王伤害', aliases=('五王伤害'), only_to_me = False, permission = perm.GROUP_ADMIN)
async def boss5_rank(session: CommandSession):
    score_str = await get_boss_info('B5')
    await session.send(score_str)   
    score_str = await get_boss_info('B5', reverse = True)
    await session.send(score_str)    
    
def tanslate2minus_sign(s):
    return re.sub(r'[_—~]', '-', s)

def arg2set(s):
    arg = tanslate2minus_sign(s)
    arg = arg.replace('，', ',')
    res = set()
    if '-' in arg:
        if re.match('[1-9]-[1-9]', arg, flags=0):
            m, M = arg.split('-')
            m, M = int(m), int(M)
            res = set([i for i in range(m, M+1)])
        else:
            res = set([i for i in range(1, -int(arg) + 1)])
    elif ',' in arg:
        arr = arg.split(',')
        res = set([int(a) for a in arr])
    else:
        res = set([int(arg)])
    return res
        
    
@score.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()
    if stripped_arg:
        try:
            # arg_arr = stripped_arg.split(maxsplit = 1)
            # arg_day = arg_arr[0]
            res = arg2set(stripped_arg)
            session.state['day_for_score'] = res
        except:
            session.state['day_for_score'] = None
            print(stripped_arg + '\t不能变成数字的样子')
    else:
        session.state['day_for_score'] = None
    return
    
    
@rank.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()
    if stripped_arg:
        try:
            res = arg2set(stripped_arg)   
            session.state['day_for_rank'] = res
        except:
            session.state['day_for_rank'] = None
            print(stripped_arg + '\t不能变成数字的样子')
    else:
        session.state['day_for_rank'] = None
    return    
