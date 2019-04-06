from pbot_utils import *
from datetime import *
from asyncio import sleep

@client.group(pass_context=True,invoke_without_command=True)
async def birthday(ctx,user=None):
    if ctx.invoked_subcommand:
        return
    if not ctx.message.raw_mentions:
        user_id = user
    else:
        user_id = ''.join(ctx.message.raw_mentions)
    member = ctx.message.server.get_member(user_id)
    if not member:
        return await client.say(":negative_squared_cross_mark: No user specified")
    usr = await (await Utils.get_server(ctx.message.server.id)).get_member(user_id)
    bday = usr.birthday
    if not bday:
        return await client.say(":broken_heart: User has not set his birthday")
    return await client.say(":birthday: **{}**'s birthday is on the **{}** of **{}**".format(member.name,bday.day,bday.strftime("%B")))

@birthday.command(pass_context=True)
async def upcoming(ctx,mon=2):
    try:
        mon = int(mon)
    except Exception:
        return await client.say(":negative_squared_cross_mark: Invalid months parameter")
    if mon<1 or mon>10:
        return await client.say(" You can only check upcoming birthdays up to 10 months")
    curr_date = datetime.now().date()
    curr_date = curr_date.replace(year=1970)
    upcm_date = (datetime.now()+timedelta(days=mon*30 if curr_date.month+mon<=12 else (12-curr_date.month)*30)).date()
    upcm_date = upcm_date.replace(year=1970)
    print(curr_date,upcm_date)
    async with db.lock:
        await db.db.execute("SELECT id,birthday FROM members WHERE server_id=%s AND birthday BETWEEN %s AND %s",(int(ctx.message.server.id),curr_date,upcm_date,))
        res = await db.db.fetchall()
    if res:
        ret = "***Upcoming birthdays in __{}__ for the next __{}__ month(s)\n\n***".format(ctx.message.server.name,mon)
        for i in res:
            try:
                ret+="⮞ __**{}**__ on the **{}** of **{}**".format(ctx.message.server.get_member(str(i[0])),i[1].day,i[1].strftime("%B"))
            except Exception:
                continue
        return await client.say(ret)
    else:
        return await client.say(":broken_heart: No upcoming birthdays in the next {} months".format(mon))

@client.command(pass_context=True)
async def setbirthday(ctx,arg=None):
    if not arg:
        return await client.say(":negative_squared_cross_mark: No date specified")
    if "/" not in arg:
        return await client.say(":negative_squared_cross_mark: Invalid date specified")
    arg = arg.split("/")
    if len(arg)<2:
        return await client.say(":negative_squared_cross_mark: No date specified")
    try:
        day = int(arg[0])
        month = int(arg[1])
    except Exception:
        return await client.say(":negative_squared_cross_mark: Invalid date specified")
    if day<1 or day>31 or month<1 or month>12:
        return await client.say(":negative_squared_cross_mark: Day or month out of range. Are you sure you provided them in the DD/MM format ?")
    usr = await (await Utils.get_server(ctx.message.server.id)).get_member(ctx.message.author.id)
    usr.birthday = datetime(1970,month,day)
    if await usr.update():
        return await client.say(":white_check_mark: You set your birthday to the **{}** of **{}**. This will only be visible in this server".format(usr.birthday.day,usr.birthday.strftime("%B")))
    await client.say(config['default_error'])

async def bday_notifs():
    tomidnight = (datetime.combine(date.today() + timedelta(1), time()) - datetime.now()).seconds
    await sleep(tomidnight)
    while True:
        try:
            today = datetime.now().date()
            today = today.replace(year=1970)
            res = await db.selectmany(table='members',fields=['id','server_id'],params={'birthday':today})
            if res:
                for i in res:
                    srv = await Utils.get_server(str(res.server_id))
                    try:
                        usr = srv.disc_server.get_member(str(res.id))
                        await client.send_message(client.get_channel(srv.event_channel),":fireworks: It's {}'s birthday today. Happy birthday {} :D".format(usr,usr.name))
                    except Exception:
                        continue
        except Exception:
            continue
        finally:
            await sleep(86400)


client.loop.create_task(bday_notifs())