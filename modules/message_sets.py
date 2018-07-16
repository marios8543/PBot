from pbot_utils import *

@client.group(pass_context=True)
async def setmessage(ctx):
    if not ctx.invoked_subcommand:
        return await client.say(":negative_squared_cross_mark: Valid channel sets are `welcome`,`goodbye`,`welcome_pm`")

@setmessage.command(pass_context=True)
async def welcome(ctx):
    if not Utils.check_perms_ctx(ctx,'manage_channels'):
        return await client.say(config['error_permissions'].format('Manage Channels'))
    server = await Utils.get_server(ctx.message.channel.server.id)    
    await client.say(":pencil: Enter your new welcome message in a triple-backtick codeblock or `cancel` to exit. \n Your current message is: \n ```{}```".format(server.entry_text))
    msg = await client.wait_for_message(timeout=240,author=ctx.message.author,channel=ctx.message.channel)
    if not msg or msg.content=='cancel':
        return await client.say(":x: Cancelled...")
    else:
        server.entry_text = msg.content[3:-3]
        if await server.update():
            return await client.say(":white_check_mark: OK that will be your new welcome message")
        else:
            return await client.say(config['default_error'])

@setmessage.command(pass_context=True)
async def goodbye(ctx):
    if not Utils.check_perms_ctx(ctx,'manage_channels'):
        return await client.say(config['error_permissions'].format('Manage Channels'))
    server = await Utils.get_server(ctx.message.channel.server.id)    
    await client.say(":pencil: Enter your new goodbye message in a triple-backtick codeblock or `cancel` to exit. \n Your current message is: \n ```{}```".format(server.goodbye_text))
    msg = await client.wait_for_message(timeout=240,author=ctx.message.author,channel=ctx.message.channel)
    if not msg or msg.content=='cancel':
        return await client.say(":x: Cancelled...")
    else:
        server.goodbye_text = msg.content[3:-3]
        if await server.update():
            return await client.say(":white_check_mark: OK that will be your new goodbye message")
        else:
            return await client.say(config['default_error'])

@setmessage.command(pass_context=True)
async def welcome_pm(ctx):
    if not Utils.check_perms_ctx(ctx,'manage_channels'):
        return await client.say(config['error_permissions'].format('Manage Channels'))
    server = await Utils.get_server(ctx.message.channel.server.id)
    print(server.entry_text_pm)
    await client.say(":pencil: Enter your new PM welcome message in a triple-backtick codeblock or `cancel` to exit. \n Your current message is: \n ```{}```".format(server.entry_text_pm))
    msg = await client.wait_for_message(timeout=240,author=ctx.message.author,channel=ctx.message.channel)
    if not msg or msg.content=='cancel':
        return await client.say(":x: Cancelled...")
    else:
        server.entry_text_pm = msg.content[3:-3]
        if await server.update():
            return await client.say(":white_check_mark: OK that will be your new PM welcome message")
        else:
            return await client.say(config['default_error'])                    