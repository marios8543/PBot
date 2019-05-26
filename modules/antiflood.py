from pbot_utils import client,db,Utils,config,logger
from asyncio import sleep

class LatestMessage:
    def __init__(self,msg):
        self.user = msg.author
        self.message = msg
        self.timestamp = msg.timestamp
        self.warns = 0
        self.dellist = []

    def update(self,msg):
        self.message = msg
        self.timestamp = msg.timestamp

class AntiFlood:
    def __init__(self,server):
        pass

servers = {}

@client.listen('on_message')
async def message_event(message):
    srv = await Utils.get_server(message.server.id)
    if not srv.af_enabled or message.author.bot:
        return
    if message.server.id not in servers:
        servers[message.server.id] = {}
    if message.channel.id not in servers[message.server.id]:
        servers[message.server.id][message.channel.id] = {}
    if message.author.id not in servers[message.server.id][message.channel.id]:
        servers[message.server.id][message.channel.id][message.author.id] = LatestMessage(message)
        return
    latest_message = servers[message.server.id][message.channel.id][message.author.id]
    latest_message.dellist.append(message)
    if (message.timestamp-latest_message.timestamp).total_seconds()<=srv.af_time:
        if len(latest_message.dellist)>=srv.af_msg:
            if latest_message.warns<=srv.af_warn or srv.af_warn<=0:
                latest_message.warns+=1
                try:
                    await client.delete_messages(latest_message.dellist)
                except Exception as e:
                    logger.error(str(e))
                try:
                    msg = await client.send_message(message.channel,":anger: Calm down <@!{}>".format(message.author.id))
                    await sleep(1)
                    await client.delete_message(msg)
                except Exception as e:
                    logger.error(str(e))
            else:
                if srv.af_warn>0:
                    invite = (await client.create_invite(message.channel,max_age=60,max_uses=1,unique=False)).url
                    await client.send_message(message.author,":exclamation: You have been kicked from **{}** for spamming. Here's a link to get back in. Be better next time\n{}".format(message.server.name,invite))
                    await client.kick(message.author)
    else:
        servers[message.server.id][message.channel.id][message.author.id].dellist = []
    servers[message.server.id][message.channel.id][message.author.id].update(message)

@client.group(pass_context=True)
async def antiflood(ctx):
    if ctx.invoked_subcommand:
        return
    server = await Utils.get_server(ctx.message.server.id)
    if server.af_enabled:
        en_str = "**enabled**"
    else:
        en_str = "**disabled**"
    return await client.say(
        """
        :information_source: __Current anti-flood settings are__:
        Message threshold: {} messages
        Time threshold: {} second(s)
        Warn threshold {} warnings
        Anti-flood is {}
        """.format(server.af_msg,server.af_time,server.af_warn,en_str)
    )

@antiflood.command(pass_context=True)
async def toggle(ctx):
    if not Utils.check_perms_ctx(ctx,'manage_channels'):
        return await client.say(config["error_permissions"].format("Manage Channels"))
    srv = await Utils.get_server(ctx.message.server.id)
    srv.af_enabled = not srv.af_enabled
    await srv.update()
    if srv.af_enabled:
        await client.say(":white_check_mark: Anti-flood has been turned on")
    else:
        await client.say(":white_check_mark: Anti-flood has been turned off")
    return

@antiflood.command(pass_context=True)
async def settime(ctx,time=None):
    if not Utils.check_perms_ctx(ctx,'manage_channels'):
        return await client.say(config["error_permissions"].format("Manage Channels"))
    if not time:
        return await client.say(":negative_squared_cross_mark: Please specify the interval between messages")
    try:
        time = int(time)
    except Exception:
        return await client.say(":negative_squared_cross_mark: Invalid seconds specified")
    srv = await Utils.get_server(ctx.message.server.id)
    srv.af_time = time
    await srv.update()
    return await client.say(":white_check_mark: Message interval has been set to {} second(s)".format(time))

@antiflood.command(pass_context=True)
async def setwarns(ctx,warns=None):
    if not Utils.check_perms_ctx(ctx,'manage_channels'):
        return await client.say(config["error_permissions"].format("Manage Channels"))
    if not warns:
        return await client.say(":negative_squared_cross_mark: Please specify the number of warnings before kicking")
    try:
        warns = int(warns)
    except Exception:
        return await client.say(":negative_squared_cross_mark: Invalid number of warnings specified")
    srv = await Utils.get_server(ctx.message.server.id)
    srv.af_warn = warns
    await srv.update()
    return await client.say(":white_check_mark: Max warnings has been set to {}".format(warns))

@antiflood.command(pass_context=True)
async def setmessages(ctx,msg=None):
    if not Utils.check_perms_ctx(ctx,'manage_channels'):
        return await client.say(config["error_permissions"].format("Manage Channels"))
    if not msg:
        return await client.say(":negative_squared_cross_mark: Please specify the number of messages needed to trigger me")
    try:
        msg = int(msg)
    except Exception:
        return await client.say(":negative_squared_cross_mark: Invalid number of messages specified")
    srv = await Utils.get_server(ctx.message.server.id)
    srv.af_msg = msg
    await srv.update()
    return await client.say(":white_check_mark: Message threshold has been set to {}".format(msg)) 