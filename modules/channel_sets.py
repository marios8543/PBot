from pbot_utils import *

#Sets the default welcome channel
@client.command(pass_context=True)
async def setwelcome(ctx):
    if Utils.check_perms_ctx(ctx,'manage_channels'):
        server = await Utils.get_server(ctx.message.channel.server.id)
        server.welcome_channel = ctx.message.channel.id
        if await server.update():
            await client.say(":white_check_mark: OK I'll log new members here")
        else:
            await client.say(config['default_error'])    
    else:
        await client.say(config['error_permissions'].format('Manage Channels'))   

#Sets the default goodbye channel
@client.command(pass_context=True)
async def setgoodbye(ctx):
    if Utils.check_perms_ctx(ctx,'manage_channels'):
        server = await Utils.get_server(ctx.message.channel.server.id)
        server.goodbye_channel = ctx.message.channel.id
        if await server.update():
            await client.say(":white_check_mark: OK I'll see leaving members off here")
        else:
            await client.say(config['default_error'])    
    else:
        await client.say(config['error_permissions'].format('Manage Channels'))

#Sets the default event channel (Namechange, announcements, etc)
@client.command(pass_context=True)
async def setevent(ctx):
    if Utils.check_perms_ctx(ctx,'manage_channels'):
        server = await Utils.get_server(ctx.message.channel.server.id)
        server.event_channel = ctx.message.channel.id
        if await server.update():
            await client.say(":white_check_mark: OK I'll show events here")
        else:
            await client.say(config['default_error'])    
    else:
        await client.say(config['error_permissions'].format('Manage Channels'))


#Sets the default logging channel
@client.command(pass_context=True)
async def setlogging(ctx):
    if Utils.check_perms_ctx(ctx,'manage_channels'):
        server = await Utils.get_server(ctx.message.channel.server.id)
        server.log_channel = ctx.message.channel.id
        if await server.update():
            await client.say(":white_check_mark: OK I'll log stuff here")
        else:
            await client.say(config['default_error'])    
    else:
        await client.say(config['error_permissions'].format('Manage Channels'))