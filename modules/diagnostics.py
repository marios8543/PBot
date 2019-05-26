from pbot_utils import *
from logging import StreamHandler
import aiohttp

task_list = {}
diag_context = {}

async def FakeContext(channel_id,message_id):
    return _FakeContext(await client.get_message(client.get_channel(str(channel_id)),str(message_id)))

class _FakeContext:
    def __init__(self,message):
        self.message = message
        self.bot = client
        self.args = [self]
        self.kwargs = {}
        self.prefix = client.command_prefix
        self.invoked_subcommand = None
        self.subcommand_passed = None


class Task:
    def __init__(self,name,code,ctx):
        self.name = name
        self.code = code
        self.ctx = ctx
        self.task = self.start(ctx=ctx)

    def stop(self):
        return self.task.cancel()

    def start(self,ctx=None):
        self.task = client.loop.create_task(execute(self.code,ctx if ctx else self.ctx))
        return self.task

    async def make_persistent(self):
        await db.insert(table="tasks",values={
            'name':self.name,
            'code':self.code,
            'message_id':self.ctx.message.id,
            'channel_id':self.ctx.message.channel.id,
            'enabled':1
        })

async def execute(code,ctx):
    # Make an async function with the code and `exec` it
    exec(
        f'async def __ex(ctx): ' +
        ''.join(f'\n {l}' for l in code.split('\n'))
    )
    return await locals()['__ex'](ctx)

async def init_tasks():
    res = await db.selectmany(table='tasks')
    for i in res:
        try:
            if i.enabled:
                task_list[i.name] = Task(i.name,i.code,FakeContext(i.channel_id,i.message_id))
                logger.info("Started persistent task {}".format(i.name))
        except Exception as e:
            logger.error("Failed to start task {} ({})".format(i.name,e))


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
    task_list[name] = Task(name,code,ctx)
    return await client.say("Task {} created".format(name))

@client.command(pass_context=True)
async def killtask(ctx,name):
    if ctx.message.author.id!="196224042988994560":
        return await client.say("Only the bot manager can use this")
    if name in task_list:
        task_list[name].stop()
        return await client.say("Task has been scheduled for cancelling")
    else:
        return await client.say("No such task")

@client.group(pass_context=True)
async def tasks(ctx):
    if ctx.invoked_subcommand:
        return
    if ctx.message.author.id!="196224042988994560":
        return await client.say("Only the bot manager can use this")
    ret = ""
    for i in task_list:
        ret+=i+'\n'
    return await client.say(ret)

@client.command(pass_context=True)
async def clear(ctx):
    if ctx.message.author.id!="196224042988994560":
        return await client.say("Only the bot manager can use this")
    for i in task_list:
        task_list[i].stop()
        tasks.pop(i,None)
    return await client.say("Stoped and erased all tasks")    

@tasks.command(pass_context=True)
async def persistent(ctx):
    if ctx.message.author.id!="196224042988994560":
        return await client.say("Only the bot manager can use this")
    res = await db.selectmany(table='tasks')
    if not res:
        return await client.say("No persistent tasks")
    ret = "Persistent tasks\n"
    for i in res:
        ret+="> {}\n".format(i.name)
    return await client.say(ret)

@tasks.command(pass_context=True)
async def make_persistent(ctx,name):
    if ctx.message.author.id!="196224042988994560":
        return await client.say("Only the bot manager can use this")
    if name in task_list:
        await task_list[name].make_persistent()
        return await client.say("Task {} made persistent".format(name))
    else:
        return await client.say("Task {} not found".format(name))

@tasks.command(pass_context=True)
async def remove_persistent(ctx,name):
    if ctx.message.author.id!="196224042988994560":
        return await client.say("Only the bot manager can use this")
    try:
        await db.delete(table='tasks',values='*',params={'name':name})
        return await client.say("Task deleted successfully")
    except:
        return await client.say("Something went wrong. Maybe the task doesn't exist ?")        


@client.command()
async def credits():
    return await client.say(config['join_msg'].format(await client.get_user_info("196224042988994560")))