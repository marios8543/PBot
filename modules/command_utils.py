from pbot_utils import *
from asyncio import sleep

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
