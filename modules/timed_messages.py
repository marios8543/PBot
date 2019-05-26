from pbot_utils import client
from asyncio import sleep

timed_users = {}

@client.listen('on_message')
async def msg_event(message):
    if message.author.id in timed_users:
        try:
            await client.add_reaction(message,"\U0001f552")
        except Exception:
            pass
        await sleep(timed_users[message.author.id])
        try:
            await client.delete_message(message)
        except Exception:
            pass


@client.command(pass_context=True)
async def timed(ctx,time=None,*msg):
    if not time:
        if ctx.message.author.id in timed_users:
            timed_users.pop(ctx.message.author.id,None)
            return await client.say(":white_check_mark: Timed messages disabled")
        return await client.say(":negative_squared_cross_mark: No time specified")
    try:
        time = int(time)
    except Exception:
        return await client.say(":negative_squared_cross_mark: Invalid time specified")
    if time>300 or time<=0:
        return await client.say(":negative_squared_cross_mark: You can't time messages more than 5 minutes")
    if len(msg)>0:
        try:
            await client.add_reaction(ctx.message,"\U0001f552")
        except Exception:
            pass
        await sleep(time)
        try:
            await client.delete_message(ctx.message)
        except Exception:
            pass
    else:
        await sleep(0.1)
        timed_users[ctx.message.author.id] = time
        return await client.say(":negative_squared_cross_mark: Timed messages enabled ({} seconds)".format(time))