from pbot_utils import *

#Turns logging on and off
@client.group(pass_context=True)
async def logging(ctx):
    if ctx.invoked_subcommand is None:
        await client.say(':negative_squared_cross_mark: Valid logging toggles are msg and name')

@logging.command(pass_context=True)
async def msg(ctx):
    if Utils.check_perms_ctx(ctx,'manage_channels'):
        server = Utils.get_server(ctx.message.server.id)
        res = server.toggle_logging_msg()
        if res==1:
            await client.say(":white_check_mark: Message change logging is now on")
            return
        elif res==2:
            await client.say(":white_check_mark: Message change logging is now off")
            return        
        else:
            await client.say(config['default_error'])    
    else:
        await client.say(config['error_permissions'].format('Manage Channels'))

@logging.command(pass_context=True)
async def name(ctx):
    if Utils.check_perms_ctx(ctx,'manage_channels'):
        server = Utils.get_server(ctx.message.server.id)
        res = server.toggle_logging_name()
        if res==1:
            await client.say(":white_check_mark: Name logging is now on")
            return
        elif res==2:
            await client.say(":white_check_mark: Name logging is now off")
            return        
        else:
            await client.say(config['default_error'])    
    else:
        await client.say(config['error_permissions'].format('Manage Channels'))            


#Message delete event
@client.event
async def on_message_delete(message):
    srv = Utils.get_server(message.server.id)
    if type(srv.log_whitelist)==list:
        whitelist=srv.log_whitelist
    else:
        whitelist = []    
    logging_whitelist = logging_blacklist + whitelist
    if srv.log_active['msg'] and str(message.author.id) not in logging_whitelist:
        if message.embeds:
            message.content = 'Cannot display embed here...'
        embed=discord.Embed(title=":exclamation: Deleted message", color=0xff0000)
        embed.add_field(name="Message author", value=str(message.author.name), inline=False)
        embed.add_field(name="Channel", value=str(message.channel.name), inline=False)
        embed.add_field(name="Content", value=str(message.content))
        embed.set_footer(text=str(message.timestamp))
        await client.send_message(client.get_channel(str(srv.log_channel)),embed=embed)

#Message edit
@client.event
async def on_message_edit(before, after):
    srv = Utils.get_server(before.server.id)
    if type(srv.log_whitelist)==list:
        whitelist=srv.log_whitelist
    else:
        whitelist = []    
    logging_whitelist = logging_blacklist + whitelist
    if srv.log_active['msg'] and str(before.author.id) not in logging_whitelist:
        if before.embeds or before.embeds:
            before.content = 'Cannot display embed here...'
            after.content = 'Cannot display embed here...'      
        embed=discord.Embed(title=":exclamation: Edited message", color=0xf4a142)
        embed.add_field(name="Message author", value=str(before.author.name+'#'+before.author.discriminator), inline=False)
        embed.add_field(name="Channel", value=str(before.channel.name))
        embed.add_field(name="Old message", value=str(before.content), inline=False)
        embed.add_field(name="New message", value=str(after.content), inline=False)
        embed.set_footer(text=str(before.timestamp))
        await client.send_message(client.get_channel(str(srv.log_channel)),embed=embed)

@client.event
async def on_member_update(before, after):
    srv = Utils.get_server(before.server.id)
    old_name = before.name
    new_name = after.name
    if srv.log_active['name'] and old_name != after.name:
        await client.send_message(client.get_channel(str(srv.event_channel)), ':anger: <@!'+before.id+'> changed their name from **'+old_name+'** to **'+after.name+'**')     