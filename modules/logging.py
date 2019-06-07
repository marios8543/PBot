from pbot_utils import *
from io import BytesIO
import aiohttp

#Turns logging on and off
@client.group(pass_context=True)
async def logging(ctx):
    if ctx.invoked_subcommand is None:
        await client.say(':negative_squared_cross_mark: Valid logging toggles are msg and name')

@logging.command(pass_context=True)
async def msg(ctx):
    if Utils.check_perms_ctx(ctx,'manage_channels'):
        server = await Utils.get_server(ctx.message.server.id)
        res = await server.toggle_logging_msg()
        if res==1:
            await client.say(":white_check_mark: Message change/delete logging is now on")
            return
        elif res==2:
            await client.say(":white_check_mark: Message change/delete logging is now off")
            return        
        else:
            await client.say(config['default_error'])    
    else:
        await client.say(config['error_permissions'].format('Manage Channels'))

@logging.command(pass_context=True)
async def name(ctx):
    if Utils.check_perms_ctx(ctx,'manage_channels'):
        server = await Utils.get_server(ctx.message.server.id)
        res = await server.toggle_logging_name()
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
    if message.channel.is_private or message.author.bot:
        return
    srv = await Utils.get_server(message.server.id)
    if not srv or not srv.log_channel:
        return    
    if type(srv.log_whitelist)==list:
        whitelist=srv.log_whitelist
    else:
        whitelist = []    
    logging_whitelist = logging_blacklist + whitelist
    if srv.log_active_message and str(message.author.id) not in logging_whitelist:
        if message.embeds:
            message.content = 'Embed below...'
        embed=discord.Embed(title=":exclamation: Deleted message", color=0xff0000)
        embed.add_field(name="Message author", value="{} (ID: {})".format(message.author,message.author.id), inline=False)
        embed.add_field(name="Channel", value=str(message.channel.name), inline=False)
        embed.add_field(name="Content", value=str(message.content if message.content else 'No message'))
        attstr = ' {} attachment(s) below'.format(len(message.attachments)) if len(message.attachments)>0 else ''
        embed.set_footer(text=str(message.timestamp)+attstr)
        await client.send_message(client.get_channel(str(srv.log_channel)),embed=embed)
        for e in message.embeds:
            await client.send_message(client.get_channel(str(srv.log_channel)),embed=e)
        for e in message.attachments:
            async with aiohttp.get(e['proxy_url']) as res:
                img = BytesIO(await res.read())
                img.seek(0)
                img.name = '{}_{}.{}'.format(message.author,message.timestamp.strftime('%d-%m-%Y_%H:%M:%S'),e['proxy_url'].split('.')[-1])
                msg = await client.send_file(client.get_channel('561545117136191501'),img)
                await client.send_message(client.get_channel(str(srv.log_channel)),msg.attachments[0]['url'])
        return

#Message edit
@client.event
async def on_message_edit(before, after):
    if before.content==after.content:
        return
    if before.channel.is_private or before.author.bot:
        return
    srv = await Utils.get_server(before.server.id)
    if not srv or not srv.log_channel:
        return
    if type(srv.log_whitelist)==list:
        whitelist=srv.log_whitelist
    else:
        whitelist = []    
    logging_whitelist = logging_blacklist + whitelist
    if srv.log_active_message and str(before.author.id) not in logging_whitelist:
        if before.embeds or before.embeds:
            before.content = '1st embed'
            after.content = '2nd embed'      
        embed=discord.Embed(title=":exclamation: Edited message", color=0xf4a142)
        embed.add_field(name="Message author", value="{} (ID: {})".format(before.author,before.author.id), inline=False)
        embed.add_field(name="Channel", value=str(before.channel.name))
        embed.add_field(name="Old message", value=str(before.content), inline=False)
        embed.add_field(name="New message", value=str(after.content), inline=False)
        embed.set_footer(text=str(before.timestamp))
        await client.send_message(client.get_channel(str(srv.log_channel)),embed=embed)
        for e in before.embeds:
            await client.send_message(client.get_channel(str(srv.log_channel)),embed=e)
        for e in after.embeds:
            await client.send_message(client.get_channel(str(srv.log_channel)),embed=e)
        return

@client.event
async def on_member_update(before, after):
    if before.name != after.name:
        srv = await Utils.get_server(before.server.id)
        if not srv:
            return
        if srv.log_active_name:
            return await client.send_message(client.get_channel(str(srv.event_channel)), ':anger: '+str(before)+' changed their name from **'+before.name+'** to **'+after.name+'**')     
