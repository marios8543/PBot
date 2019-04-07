from pbot_utils import *

#Member join event
@client.event
async def on_member_join(member):
    server = member.server
    srv = await Utils.get_server(server.id)
    if "/" in member.name and "." in member.name:
        await client.send_message(member,":exclamation: You have been auto-banned for suspected botting. If you believe this was done by mistake message **tzatzikiweeb#7687**")
        await client.send_message(client.get_channel(str(srv.log_channel)),":exclamation: RaidBot prevention `{}`".format(str(member)))
        return await client.ban(member)
    unverified = discord.utils.get(server.roles, name="Unverified")
    try:
        await client.add_roles(member, unverified)
    except:
        client.send_message(":exclamation: Coulnd't assign Unverified role. Check permissions...")
        pass
    await client.send_message(client.get_channel(str(srv.welcome_channel)),srv.entry_text.format(**{'member_name':member.name,'server_name':server.name}))
    msg = await client.send_message(member,srv.entry_text_pm.format(**{'member_name':member.name,'server_name':server.name}))
    await client.add_reaction(msg,'\U0001f44d')
    await asyncio.sleep(1)
    usr = await srv.get_member(member.id)
    if not usr:
        usr = await srv.make_member(member.id)
    else:
        usr.verified = 0
        await usr.update()
    while True:
        res = await client.wait_for_reaction(message=msg)
        if not res:
            continue
        if res.reaction.emoji == '\U0001f44d':
            await client.remove_roles(member,unverified)
            await client.send_message(member,':white_check_mark: You have been verified. Enjoy your stay :champagne:')
            await client.send_message(client.get_channel(str(srv.event_channel)),":champagne: **{}** has just been verified. Welcome to the server **{}** :D".format(str(member),member.name))
            usr.verified = 1
            await usr.update()


#Member leave event
@client.event
async def on_member_remove(member):
    if "/" in member.name and "." in member.name:
        return
    srv = await Utils.get_server(member.server.id)
    await client.send_message(client.get_channel(str(srv.goodbye_channel)),srv.goodbye_text.format(member.name+'#'+member.discriminator))
    await db.update(table='members',values={'in_server':'0'},params={'id':member.id,'server_id':member.server.id})