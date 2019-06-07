from pbot_utils import *
from asyncio import sleep,Lock

@client.event
async def on_command_completion(command,ctx):
    if not ctx.message.channel.is_private:
        chstr = "in {} (ID:{}) on {} (ID:{})".format(ctx.message.channel.name,ctx.message.channel.id,ctx.message.server.name,ctx.message.server.id)
    else:
        chstr = "in PM"
    logger.info("{} (ID:{}) called {} {}".format(ctx.message.author,ctx.message.author.id,command.name,chstr))
    srv = await Utils.get_server(ctx.message.server.id)
    if srv:
        async with db.lock:
            await db.db.execute("UPDATE commands SET usages = usages+1 WHERE command=%s AND server_id=%s",(command.name,ctx.message.server.id,))

@client.group(pass_context=True)
async def analytics(ctx):
    if not Utils.check_perms_ctx(ctx,'manage_messages'):
        return await client.say(config['error_permissions'].format('Manage Messages'))
    if ctx.invoked_subcommand:
        return
    async with db.lock:
        await db.db.execute("SELECT * FROM commands WHERE server_id=%s ORDER BY usages DESC",(ctx.message.server.id,))
        res = await db.db.fetchall()
    if res and len(res)>0:
        msg_str = "***Command usage analytics for {}***\n".format(ctx.message.server.name)
        for i in res:
            msg_str+="`{}: {} usages`\n".format(i[0],i[1])
        return await client.say(msg_str)