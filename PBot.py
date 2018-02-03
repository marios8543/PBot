import json
import discord
import asyncio
import mysql.connector
from datetime import datetime
from discord.ext.commands import Bot
from discord.ext import commands
import lxml.html
from urllib.request import urlopen
import hashlib
from random import randint
import time
import codecs

warn_whitelist=['196224042988994560','180800780960399361','207559404466208779','386505899713495051']
logging_blacklist=['196224042988994560','351236161684897792','381066546535202816']

#Create database connection
conn = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='pbot')
db = conn.cursor(buffered=True)

#Initial database caching
db.execute("SELECT server_id,welcome_channel,goodbye_channel,event_channel,log_channel,log_msgchanges,log_whitelist,entry_text,goodbye_text,entry_text_pm FROM servers")
data = db.fetchall()
w_channels = {}
g_channels = {}
e_channels = {}
l_channels = {}
log_status = {}
log_wlists = {}
w_txt = {}
g_txt = {}
wpm_txt = {}
for srv in data:
    w_channels[str(srv[0])] = str(srv[1])
    g_channels[str(srv[0])] = str(srv[2])
    e_channels[str(srv[0])] = str(srv[3])
    l_channels[str(srv[0])] = str(srv[4])
    log_status[str(srv[0])] = str(srv[5])
    log_wlists[str(srv[0])] = str(srv[6].decode('utf-8'))
    w_txt[str(srv[0])] = str(srv[7].decode('utf-8'))
    g_txt[str(srv[0])] = str(srv[8].decode('utf-8'))
    wpm_txt[str(srv[0])] = str(srv[9].decode('utf-8'))

#Function for removing non-ascii characters that can't be stored in the database
def remove_non_ascii(text):
    return ''.join([i if ord(i) < 128 else ' ' for i in str(text)])

#Initial setup
client = Bot(description="pbot_public", command_prefix=">>")
@client.event
async def on_ready():
    print('Logged in as '+client.user.name+' (ID:'+client.user.id+') | Connected to '+str(len(client.servers))+' servers | Connected to '+str(len(set(client.get_all_members())))+' users github.com/marios8543/PBot/')
    await client.change_presence(game=discord.Game(name="DON'T type >>help"))


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

#Verify command to be used in conjuction with entry forms (D E P R E C A T E D)
#@client.command(pass_context=True)
async def verify(ctx, member: discord.Member = None):
 member2 = ctx.message.author
 server = ctx.message.server
 member2server = server.get_member(member2.id)
 unverified = discord.utils.get(server.roles, name="Unverified")
 if unverified in member2server.roles:
  db.execute("""SELECT verified from members WHERE discord_id=%s AND server_id=%s""",(str(member2.id), str(server.id)))
  verified_status = db.fetchone()
  if verified_status[0] is 1:
        await client.remove_roles(member2server, unverified)
        await client.say(':white_check_mark: You have been verified. Enjoy your stay :champagne:')
  else:
        await client.say(':negative_squared_cross_mark: Please fill in the form first. Check your PMs')
 else:
  await client.say(':negative_squared_cross_mark: You are already verified')

#Agree command to be used in non entry-form scenarios (D E P R E C A T E D)
#client.command(pass_context=True)
async def agree(ctx):
 db.execute("SELECT entry_form from servers WHERE server_id="+str(ctx.message.server.id))
 uses_form = db.fetchone()[0]
 if uses_form == 0:
      server = ctx.message.server
      member2 = ctx.message.author
      member2server = server.get_member(member2.id)
      unverified = discord.utils.get(server.roles, name="Unverified")
      if unverified in member2server.roles:
          await client.remove_roles(member2server,unverified)
          await client.say(':white_check_mark: You have been verified. Enjoy your stay :champagne:')
          db.execute("""UPDATE members SET verified=1 WHERE discord_id=%s AND server_id=%s""",(str(member2.id), str(server.id)))
          conn.commit()
 else:
     await client.say(":negative_squared_cross_mark: This server uses an entrance form system. Please check your DMs for more info or contact an admin")


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


@client.command(pass_context=True)
async def clearwarnings(ctx,arg):
 server = ctx.message.server
 if ctx.message.author.server_permissions.ban_members == True:
     user2check = ctx.message.raw_mentions
     user_id = ''.join(user2check)
     print(str(ctx.message.author.id))
     print(str(server.id))
     db.execute("""UPDATE members SET warns=0 WHERE discord_id=%s AND server_id=%s""",(user_id,int(server.id)))
     conn.commit()
     await client.say(':white_check_mark: <@!'+user_id+'> is now clear!')
 else:
     await client.say(':negative_squared_cross_mark: Only admins can use this!')

@client.command()
async def ping():
 timestamp = datetime.now()
 msg = await client.say('I work!!!')
 msg_time = msg.timestamp
 result = timestamp - msg_time
 result = result.total_seconds()
 await client.edit_message(msg,'I work!!! `'+str(result)+'sec`')
 sql_result = conn.ping()
 await client.say(str(sql_result))

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


@client.command(pass_context=True)
async def chelp(ctx):
  command_list = open("command_list.txt",'r').read()
  await client.send_message(ctx.message.author,command_list)
  await client.say(':white_check_mark: Help has been slid in your DMs')

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


@client.command()
async def bsf():
 dolartoday = urlopen('https://s3.amazonaws.com/dolartoday/data.json').read().decode('cp1252')
 result = json.loads(dolartoday)
 price = result['USD']['promedio']
 embed = discord.Embed(Title='USD', color=0xf4f142)
 embed.set_author(name='Venezuelan Bolivar',icon_url='https://cdn.urgente24.com/sites/default/files/notas/2015/05/29/maduro-risa-425x318.jpg')
 embed.add_field(name='1USD is...', value=str(price)+' Bs.F')
 embed.set_footer(text="This isn't real socialism")
 await client.say(embed=embed)


@client.command()
async def emoji(emoji):
 emoji_id = str(emoji)[-19:]
 emoji_id = emoji_id[:-1]
 await client.say('https://cdn.discordapp.com/emojis/'+emoji_id+'.png')

#def exit_backup():



token = open("token.txt",'r').read()
client.run(token)
