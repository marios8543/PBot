from pbot_utils import *

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
            if msg.content.split(" ")[0]=="/a":
                cl = " ".join(msg.content.split(" ")[1:])
                await client.say(await eval(cl))
            else:
                cl = msg.content
                await client.say(eval(cl))
        except Exception as e:
            await client.say("Error ({})".format(str(e)))
        
@client.command()
async def credits():
    return await client.say(config['join_msg'].format(await client.get_user_info("196224042988994560")))