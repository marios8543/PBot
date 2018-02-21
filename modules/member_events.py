#Member join event
@client.event
async def on_member_join(member):
 server = member.server
 member_non_ascii = remove_non_ascii(member)
 unverified = discord.utils.get(server.roles, name="Unverified")
 await client.add_roles(member, unverified)
 timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
 db.execute("""INSERT into members (discord_name,discord_id,server_id,join_date,verified,in_server) values(%s,%s,%s,%s,0,1)""",(str(member_non_ascii), int(member.id),int(server.id),timestamp))
 conn.commit()
 welcome_channel = w_channels[str(server.id)]
 entry_text = w_txt[str(server.id)]
 entry_text_pm = wpm_txt[str(server.id)]
 entry_form = 0
 await client.send_message(client.get_channel(str(welcome_channel)),str(entry_text).format(str(member.name),str(member.server.name)))
 if entry_form==0:
      msg = await client.send_message(member,str(entry_text_pm))
      await client.add_reaction(msg,'👍')
      await asyncio.sleep(1)
      res = await client.wait_for_reaction(message=msg)
      if res.reaction.emoji == '👍':
          await client.remove_roles(member,unverified)
          await client.send_message(member,':white_check_mark: You have been verified. Enjoy your stay :champagne:')
 else:
     await client.send_message(member,'!USES FORM! '+entry_text_pm)


#Member leave event
@client.event
async def on_member_remove(member):
 db.execute("""UPDATE members SET in_server=0 WHERE discord_id=%s AND server_id=%s""",(str(member.id), str(member.server.id)))
 goodbye_channel = g_channels[str(member.server.id)]
 goodbye_text = g_txt[str(member.server.id)]
 await client.send_message(client.get_channel(str(goodbye_channel)), str(goodbye_text).format(str(member.name)))
