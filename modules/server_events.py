from pbot_utils import *
import random

#Server join event
@client.event
async def on_server_join(server):
    for channel in server.channels:
        if 'general' in channel.name:
            destination = channel
            break
    if not destination:
        destination = random.choice(server.channels)        
    srv = await Utils.make_server(id=server.id)
    await client.send_message(destination,config['join_msg'])
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