#Member namechange event
@client.event
async def on_member_update(before, after):
 event_channel = e_channels[str(before.server.id)]
 user_id = before.id
 old_name = before.name
 new_name = after.name+'#'+after.discriminator
 new_name = remove_non_ascii(new_name)
 new_name_store = new_name.replace(" ", "_")
 if old_name != after.name:
  await client.send_message(client.get_channel(str(event_channel)), ':anger: <@!'+user_id+'> changed their name from **'+old_name+'** to **'+after.name+'**')
  db.execute("""UPDATE members SET discord_name=%s WHERE discord_id=%s AND server_id=%s""",(str(new_name_store), user_id, before.server.id))
  conn.commit()

#Message delete event
@client.event
async def on_message_delete(message):
 active = log_status[str(message.server.id)]
 whitelist = log_wlists[str(message.server.id)]
 whitelist = json.loads(whitelist)
 logging_whitelist = logging_blacklist + whitelist
 if active == '1' and str(message.author.id) not in logging_whitelist:
     dest = l_channels[str(message.server.id)]
     embed=discord.Embed(title=":exclamation: Deleted message", color=0xff0000)
     embed.add_field(name="Message author", value=str(message.author.name), inline=False)
     embed.add_field(name="Channel", value=str(message.channel.name), inline=False)
     embed.add_field(name="Content", value=str(message.content))
     embed.set_footer(text=str(message.timestamp))
     await client.send_message(client.get_channel(str(dest)),embed=embed)
 else:
     print('Not logging')


#Message edit
@client.event
async def on_message_edit(before, after):
    active = log_status[str(before.server.id)]
    whitelist = log_wlists[str(before.server.id)]
    whitelist = json.loads(whitelist)
    logging_whitelist = logging_blacklist + whitelist
    if active == '1' and str(before.author.id) not in logging_whitelist:
        dest = l_channels[str(before.server.id)]
        message_id = before.id
        message_author = before.author.name
        channel = before.channel.name
        old_content = before.content
        new_content = after.content
        timestamp = before.timestamp
        embed=discord.Embed(title=":exclamation: Edited message", color=0xf4a142)
        embed.add_field(name="Message author", value=str(message_author), inline=False)
        embed.add_field(name="Channel", value=str(channel))
        embed.add_field(name="Old message", value=str(old_content), inline=False)
        embed.add_field(name="New message", value=str(new_content), inline=False)
        embed.set_footer(text=str(timestamp))
        await client.send_message(client.get_channel(str(dest)),embed=embed)
    else:
        print('Not logging')
