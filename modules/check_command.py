#member check command
@client.command(pass_context=True)
async def check(ctx, arg):
 server = ctx.message.server
 member2 = ctx.message.author
 permissions = member2.server_permissions
 if permissions.ban_members == True:
     user2check = ctx.message.raw_mentions
     user_id = ''.join(user2check)
     db.execute("SELECT discord_name from members WHERE discord_id="+user_id)
     discord_name = db.fetchone()[0]
     db.execute("SELECT warns from members WHERE discord_id="+user_id)
     warning_count = db.fetchone()[0]
     join_date = server.get_member(user_id).joined_at
     top_role = server.get_member(user_id).top_role
     embed = discord.Embed(title=':mag: >PBot User Lookup', color=0xc242f4)
     embed.add_field(name='Discord Name', value=arg, inline=False)
     embed.add_field(name='Discord ID', value=user_id, inline=False)
     embed.add_field(name='Name in DB', value=discord_name, inline=False)
     embed.add_field(name='Join Date', value=join_date, inline=False)
     embed.add_field(name='Warning Count', value=warning_count, inline=False)
     embed.add_field(name='Highest rank', value=top_role, inline=False)
     embed.set_footer(text='Requested by '+str(member2)+' on '+str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
     await client.send_message(member2,embed=embed)
     await client.say(":white_check_mark: The user's report card has been sent in your DMs")
 else:
     await client.say(':negative_squared_cross_mark: Only users with the `Ban Members` can use this!')
