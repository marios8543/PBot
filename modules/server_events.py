from pbot_utils import *
from discord.enums import ChannelType
import random

#Server join event
@client.event
async def on_server_join(server):
    destination = None
    for i in server.channels:
        if i.type==ChannelType.text and i.permissions_for(server.get_member(client.user.id)).send_messages:
            destination = i
            break
    if not destination:
        await client.leave_server(server)
    srv = await Utils.make_server(id=server.id)
    await client.send_message(destination,config['join_msg'].format(await client.get_user_info("196224042988994560")))
    await client.send_message(destination,"I'll now log all the members in this server to make my work easier...")
    await client.send_typing(destination)
    member_count = 0
    for member in server.members:
        if await srv.make_member(member.id,verified=1):
            member_count = member_count+1
        else:
            await client.send_message(destination,'Could not add member {} (ID:{})'.format(member.name,member.id))
    await client.send_message(destination,'Successfully added {} members'.format(member_count))
    await client.send_message(destination,"Ok I think I'm done for now. Go to {}/setup for help on further setting up >PBot".format(config['url']))


#Server leave event
@client.event
async def on_server_remove(server):
    await Utils.delete_server(server.id)