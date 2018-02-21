#Warn command
@client.command(pass_context=True)
async def warn(ctx,user,reason):
 server = ctx.message.server
 member2 = ctx.message.author
 permissions = member2.server_permissions
 if permissions.ban_members == True:
     user2check = ctx.message.raw_mentions
     user_id = ''.join(user2check)
     warnman = server.get_member(str(user_id))
     if str(user_id) not in warn_whitelist:
              db.execute("SELECT max_warns from servers WHERE server_id="+str(server.id))
              max_warns = db.fetchone()[0]
              db.execute("SELECT warns from members WHERE discord_id="+user_id)
              warns = db.fetchone()[0]
              print(str(warns))
              print(str(max_warns))
              if int(warns)+1 != int(max_warns):
                  timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                  db.execute("""UPDATE members SET warns=%s WHERE discord_id=%s AND server_id=%s""",(int(warns)+1, user_id,str(server.id)))
                  db.execute("""INSERT INTO warnings (discord_name,discord_id,server_id,warn_datetime,admin,reason) values(%s,%s,%s,%s,%s,%s)""",(str(warnman.name+str(warnman.discriminator)),int(user_id),int(server.id),timestamp,str(ctx.message.author.name+ctx.message.author.discriminator),reason))
                  conn.commit()
                  await client.say(':exclamation: <@!'+str(user_id)+'> has been warned. His warning count is now '+str(warns+1)+' ('+str(int(max_warns)-int(warns) -1)+' warns left)')
                  embed=discord.Embed(title=":exclamation: User Warned", color=0xed00f9)
                  embed.add_field(name="User warned", value=warnman.name+'#'+str(warnman.discriminator), inline=False)
                  embed.add_field(name="Admin in charge", value=ctx.message.author.name, inline=False)
                  embed.add_field(name="Reason", value=reason, inline=False)
                  embed.add_field(name="Warning count", value=str(warns+1)+' ('+str(int(max_warns)-int(warns) -1)+' warns left)', inline=False)
                  embed.set_footer(text=str(timestamp))
                  dest = l_channels[str(server.id)]
                  await client.send_message(client.get_channel(str(dest)),embed=embed)
              else:
                  member2server = server.get_member(user_id)
                  msg = await client.say(':exclamation: User has 3 warnings and will be banned! Click on :white_check_mark: to confirm...')
                  await client.add_reaction(msg,'👍')
                  await asyncio.sleep(1)
                  res = await client.wait_for_reaction(message=msg)
                  if res.reaction.emoji == '👍':
                      await client.ban(member2server)
                      await client.send_message(client.get_user_info(user_id),'You have been banned for breaking the rules. You totally received '+str(warns)+' warnings before being issued a ban.')


     else:
         await client.say(':negative_squared_cross_mark: Haha nice try cuck. You cant warn me :^)')
 else:
     await client.say(':negative_squared_cross_mark: Only admins can use this!')

#Clear warnings
@client.command(pass_context=True)
async def clearwarnings(ctx,arg):
 server = ctx.message.server
 if ctx.message.author.server_permissions.ban_members == True:
     user2check = ctx.message.raw_mentions
     user_id = ''.join(user2check)
     db.execute("""UPDATE members SET warns=0 WHERE discord_id=%s AND server_id=%s""",(user_id,int(server.id)))
     conn.commit()
     await client.say(':white_check_mark: <@!'+user_id+'> is now clear!')
 else:
     await client.say(':negative_squared_cross_mark: Only admins can use this!')


#Softban/Mute command
@client.command(pass_context=True)
async def softban(ctx,arg,arg2):
 server = ctx.message.server
 member2 = ctx.message.author
 permissions = member2.server_permissions
 if permissions.ban_members == True:
    if int(arg2) <= 60:
      unverified = discord.utils.get(server.roles, name="Unverified")
      user2check = ctx.message.raw_mentions
      user_id = ''.join(user2check)
      time = int(arg2)*60
      await client.add_roles(server.get_member(user_id), unverified)
      await client.say(':white_check_mark: <@!'+str(user_id)+'> has been denied access for '+str(arg2)+' minutes...')
      await asyncio.sleep(time)
      await client.remove_roles(server.get_member(user_id), unverified)
      await client.say('<@!'+str(user_id)+'> is here again!')
    else:
      await client.say(':negative_squared_cross_mark: Maximum softban time is 60 minutes')

 else:
     await client.say(':negative_squared_cross_mark: Only members with the `Ban Members` can use this!')

#Manual verification command
@client.command(pass_context=True)
async def verify(ctx,arg):
 server = ctx.message.server
 member2 = ctx.message.author
 permissions = member2.server_permissions
 if permissions.ban_members == True:
     unverified = discord.utils.get(server.roles, name="Unverified")
     user2check = ctx.message.raw_mentions
     user_id = ''.join(user2check)
     db.execute("""UPDATE members SET verified=1 WHERE discord_id=%s AND server_id=%s""",(str(member2.id),str(server.id)))
     conn.commit()
     await client.remove_roles(server.get_member(user_id), unverified)
     await client.say(':white_check_mark: Manually verified <@!'+str(user_id)+'> !')
 else:
     await client.say(':negative_squared_cross_mark: Only members with the `Ban Members` can use this!')

#Sets the nickname for someone
@client.command(pass_context=True)
async def nickname(ctx,name,nick):
 server = ctx.message.server
 member2 = ctx.message.author
 permissions = member2.server_permissions
 if permissions.manage_nicknames == True:
     user2check = ctx.message.raw_mentions
     user_id = ''.join(user2check)
     await client.change_nickname(server.get_member(str(user_id)), str(nick))
     await client.say(":white_check_mark: Successfully changed <@!"+user_id+">'s nickname to **"+str(nick)+"**")
 else:
     await client.say(":negative_squared_cross_mark: Only members with the `Manage Nicknames` permission can use this!")

#Massdelete messages
@client.command(pass_context=True)
async def massdelete(ctx,msgfrom,msgto):
 del_msg_count = 0
 server = ctx.message.server
 channel = ctx.message.channel
 message_after = await client.get_message(channel,msgfrom)
 message_before = await client.get_message(channel,msgto)
 member2 = ctx.message.author
 permissions = member2.server_permissions
 if permissions.manage_messages == True:
      del_list = await client.purge_from(channel=channel,limit=100, check=None, before=message_before, after=message_after, around=None)
      print(str(del_list))
      await client.say(':white_check_mark: Successfully deleted '+str(len(del_list))+' messages !')
 else:
    await client.say(':negative_squared_cross_mark: Only members with the `Manage Messages` permission can use this!')


#Access the dashboard for your server
@client.command(pass_context=True)
async def dashboard(ctx):
    if ctx.message.author.server_permissions.manage_server == True:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            author_id = str(ctx.message.author.id)
            author_name = str(ctx.message.author.name+ctx.message.author.discriminator)
            server_id = str(ctx.message.server.id)
            random = str(randint(1000000000,9999999999))
            tobehashed = str(author_id+server_id+random).encode("utf-8")
            hash_object = hashlib.sha1(tobehashed)
            hash_res = hash_object.hexdigest()
            db.execute("""INSERT INTO setting_sessions (id,token,server_id,admin_id,admin_name,timestamp,valid) values(%s,%s,%s,%s,%s,%s,1)""",(random,hash_res,server_id,author_id,author_name,timestamp))
            conn.commit()
            my_ip = 'https://nue.thebit.link/pbot'
            embed = discord.Embed(Title="set_session")
            embed.set_author(name=">PBot Dashboard Session",icon_url="https://raw.githubusercontent.com/marios8543/Implying_Pbot/master/kamina.png")
            embed.add_field(name="Click here to go to settings",value=my_ip+"/session.php?token="+hash_res)
            embed.set_footer(text="New dashboard coming soon...")
            await client.send_message(ctx.message.author,embed=embed)
            await client.say(":white_check_mark: Check your DMs to change the bot's settings...")
    else:
        await client.say(":negative_squared_cross_mark: Only members with the `Manage Server` permission can change the bot settings")     
