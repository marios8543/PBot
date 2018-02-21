#Server join event
@client.event
async def on_server_join(server):
 server_owner = server.owner
 timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
 db.execute("""INSERT into servers (server_id,server_name,added_on,entry_text,entry_text_pm,goodbye_text,log_whitelist) values(%s,%s,%s,"Greetings, **{0}**. Welcome to ***{1}***. Enjoy your stay ! ","This is a sample text. Fill in the form and type `>>verify` to gain access to the server","A'ight farewell **{}**...",%s)""",(server.id, server.name, timestamp,'["0"]'))
 conn.commit()
 msg = await client.send_message(server_owner,"`Hey I'm >PBot. Thanks for inviting me to your server. Read the TOS and react with 👍 to this message to continue" )
 res = await client.wait_for_reaction(['👍'], message=msg)
 if res.reaction.emoji == '👍':
     await client.send_message(server_owner, "I'll start by storing all the members in my database since that will make my job easier")
     member_count = 0
     for member in server.members:
         member_non_ascii = remove_non_ascii(member)
         server_id = server.id
         member_id = member.id
         timestamp = member.joined_at
         db.execute("""INSERT into members (discord_name,discord_id,server_id,join_date,verified,in_server) values(%s,%s,%s,%s,1,1)""",(str(member_non_ascii), int(member_id),int(server_id), timestamp,))
         conn.commit()
         member_count = member_count + 1
     await client.send_message(server_owner,"A'ight I just added "+str(member_count)+" members in the database!")
     command_list = open("command_list.txt",'r').read()
     await client.send_message(server_owner, command_list)
 else:
     await client.send_message(server_owner,"Well that's too bad. Guess I'll just leave then :/")
     await client.leave_server(server)

#Server leave event
@client.event
async def on_server_remove(server):
    server_id = server.id
    db.execute("DELETE FROM servers WHERE server_id="+str(server_id))
    db.execute("DELETE FROM members WHERE server_id="+str(server_id))
    db.execute("DELETE FROM warnings WHERE server_id="+str(server_id))
    conn.commit()
