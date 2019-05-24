from pbot_utils import *
import aiohttp

task_list = {}
diag_context = {}

async def execute(code,ctx):
    # Make an async function with the code and `exec` it
    exec(
        f'async def __ex(ctx): ' +
        ''.join(f'\n {l}' for l in code.split('\n'))
    )
    return await locals()['__ex'](ctx)

@client.command(pass_context=True)
async def interpret(ctx):
    if ctx.message.author.id!="196224042988994560":
        return await client.say("Only the bot manager can use this")
    await client.say("Switching on interpreter mode")
    while True:
        msg = await client.wait_for_message(author=ctx.message.author,channel=ctx.message.channel)
        if not msg:
            continue
        if msg.content=="quit":
            return await client.say("Exiting interpreter mode")
        try:
            resp = await execute(msg.content,ctx)
            if not resp:
                await client.say("Evaluation returned None")
            else:
                await client.say(resp)
        except Exception as e:
            await client.say("Error ({})".format(str(e)))


@client.command(pass_context=True)
async def addtask(ctx,name=None,link=None):
    if ctx.message.author.id!="196224042988994560":
        return await client.say("Only the bot manager can use this")    
    if not name:
        return await client.say("Your task requires a name")
    if name in task_list:
        return await client.say("Task with this name already exists")
    code = None
    if link:
        if link.split(".")[-1]=="py":
            async with aiohttp.get(link) as res:
                if res.status==200:
                    code = await res.text()
                else:
                    return await client.say("Something went wrong fetching your code")
        else:
            return await client.say("Link must point to a python file")
    else:
        await client.say("Send your code in triple backticks")
        msg = await client.wait_for_message(timeout=300,author=ctx.message.author,channel=ctx.message.channel)
        if msg.content == 'cancel':
            return await client.say(':x: Cancelled...')
        if msg == None:
            return await client.say(':zzz: Timed out...') 
        code = msg.content[3:-3]
    if not code:
        return await client.say("No code")
    task_list[name] = client.loop.create_task(execute(code,ctx))
    return await client.say("Task {} created".format(name))

@client.command(pass_context=True)
async def killtask(ctx,name):
    if ctx.message.author.id!="196224042988994560":
        return await client.say("Only the bot manager can use this")
    if name in task_list:
        task_list[name].cancel()
        task_list.pop(name,None)
        return await client.say("Task has been scheduled for cancelling")
    else:
        return await client.say("No such task")

@client.command(pass_context=True)
async def tasks(ctx):
    if ctx.message.author.id!="196224042988994560":
        return await client.say("Only the bot manager can use this")
    ret = ""
    for i in task_list:
        ret+=i+'\n'
    return await client.say(ret)    



@client.command()
async def credits():
    return await client.say(config['join_msg'].format(await client.get_user_info("196224042988994560")))