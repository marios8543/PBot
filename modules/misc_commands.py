#Ping command
@client.command()
async def ping():
 timestamp = datetime.now()
 msg = await client.say('I work!!!')
 msg_time = msg.timestamp
 result = timestamp - msg_time
 result = result.total_seconds()
 await client.edit_message(msg,'I work!!! `'+str(result)+'sec`')
 sql_result = conn.ping()
 await client.say('MySQL status is: '+str(sql_result))


#Help command
@client.command(pass_context=True)
async def chelp(ctx):
  command_list = open("command_list.txt",'r').read()
  await client.send_message(ctx.message.author,command_list)
  await client.say(':white_check_mark: Help has been slid in your DMs')
