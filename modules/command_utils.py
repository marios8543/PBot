from pbot_utils import *
from asyncio import sleep,Lock

@client.event
async def on_command_completion(command,ctx):
    srv = await Utils.get_server(ctx.message.server.id)
    if srv:
        if 'delete_command' in srv.log_active:
            if srv.log_active['delete_command']=="1":
                await sleep(3)
                await client.delete_message(ctx.message)
        else:
            srv.log_active['delete_command']="0"
            await srv.update()
        async with db.lock:
            await db.db.execute("UPDATE commands SET usages = usages+1 WHERE command=%s AND server_id=%s",(command.name,ctx.message.server.id,))
            await db.db.execute("UPDATE commands SET usages = usages+1 WHERE command=%s",(command.name,))

@client.command(pass_context=True)
async def setdelete(ctx):
    if Utils.check_perms_ctx(ctx,'manage_channels'):
        srv = await Utils.get_server(ctx.message.server.id)
        if srv:
            if 'delete_command' in srv.log_active:
                if srv.log_active['delete_command']=="1":
                    srv.log_active['delete_command'] = "0"
                    await client.say(":white_check_mark: Command calls will now stop being deleted")
                else:
                    srv.log_active['delete_command'] = "1"
                    await client.say(":white_check_mark: Command calls will now be deleted")
            else:
                srv.log_active['delete_command']="0"
            await srv.update()
    else:
        await client.say(config['error_permissions'].format('Manage Channels'))

@client.group(pass_context=True)
async def analytics(ctx):
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

@analytics.command(pass_context=True)
async def bot(ctx):
    async with db.lock:
        await db.db.execute("SELECT * FROM commands WHERE server_id=%s ORDER BY usages DESC",(None,))
        res = await db.db.fetchall()
        print(res)
    if res and len(res)>0:
        msg_str = "***Command usage analytics for {}***\n".format(ctx.message.server.name)
        for i in res:
            msg_str+="`{}: {} usages`\n".format(i[0],i[1])
        return await client.say(msg_str)