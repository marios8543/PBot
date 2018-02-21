#Sets the default welcome channel
@client.command(pass_context=True)
async def setwelcome(ctx):
 server = ctx.message.server
 member = server.get_member(ctx.message.author.id)
 permissions = member.server_permissions
 if permissions.manage_server == True:
      await client.say(':white_check_mark: Alrightie. Ill greet all the newcomers here...')
      w_channels[str(server.id)] = str(ctx.message.channel.id)
      db.execute("""UPDATE servers set welcome_channel=%s WHERE server_id=%s""", (int(ctx.message.channel.id), int(ctx.message.server.id)))
      conn.commit()
 else:
      await client.say(":negative_squared_cross_mark: Only members with the `Manage Server` permission can use this")

#Sets the default goodbye channel
@client.command(pass_context=True)
async def setgoodbye(ctx):
 server = ctx.message.server
 member = server.get_member(ctx.message.author.id)
 permissions = member.server_permissions
 if permissions.manage_server == True:
      await client.say(':white_check_mark: Alrightie. Ill rid all the leaving faggots here...')
      g_channels[str(server.id)] = str(ctx.message.channel.id)
      db.execute("""UPDATE servers set goodbye_channel=%s WHERE server_id=%s""", (int(ctx.message.channel.id), int(ctx.message.server.id)))
      conn.commit()
 else:
      await client.say(":negative_squared_cross_mark: Only members with the `Manage Server` permission can use this")

#Sets the default event channel (Namechange, announcements, etc)
@client.command(pass_context=True)
async def setevent(ctx):
 server = ctx.message.server
 member = server.get_member(ctx.message.author.id)
 permissions = member.server_permissions
 if permissions.manage_server == True:
      await client.say(":white_check_mark: A'ight this will be the default event channel from now on...")
      e_channels[str(server.id)] = str(ctx.message.channel.id)
      db.execute("""UPDATE servers SET event_channel=%s WHERE server_id=%s""",(int(ctx.message.channel.id), int(ctx.message.server.id)))
      conn.commit()
 else:
      await client.say(":negative_squared_cross_mark: Only members with the `Manage Server` permission can use this")


#Sets the default logging channel
@client.command(pass_context=True)
async def setlogging(ctx):
 server = ctx.message.server
 member = server.get_member(ctx.message.author.id)
 permissions = member.server_permissions
 if permissions.manage_server == True:
      l_channels[str(server.id)] = str(ctx.message.channel.id)
      await client.say(':white_check_mark: Alrightie. Ill log stuff here...')
      db.execute("""UPDATE servers set log_channel=%s WHERE server_id=%s""", (int(ctx.message.channel.id), int(ctx.message.server.id)))
      conn.commit()

 else:
      await client.say(":negative_squared_cross_mark: Only members with the `Manage Server` permission can use this")

#Turns message logging on and off
@client.command(pass_context=True)
async def logging(ctx):
 server = ctx.message.server
 member = server.get_member(ctx.message.author.id)
 permissions = member.server_permissions
 if permissions.manage_server == True:
     result = log_status[str(server.id)]
     if result == '0':
         await client.say(':white_check_mark: Message change logging is now on!')
         db.execute("UPDATE servers SET log_msgchanges=1 WHERE server_id="+str(server.id))
         log_status[str(server.id)] = '1'
     else:
         await client.say(':white_check_mark: Message change logging is now off!')
         db.execute("UPDATE servers SET log_msgchanges=0 WHERE server_id="+str(server.id))
         log_status[str(server.id)] = '0'
 else:
     await client.say(":negative_squared_cross_mark: Only members with the `Manage Server` permission can use this")
