from pbot_utils import *
import xml.etree.ElementTree as xml
import random
import aiohttp
from time import strptime
from datetime import datetime
import time
import math

@client.command()
async def bsf():
    async with aiohttp.get('https://s3.amazonaws.com/dolartoday/data.json')as dolartoday:
        result = await dolartoday.json(encoding='cp1252')
        price = result['USD']['promedio']
        embed = discord.Embed(Title='USD', color=0xf4f142)
        embed.set_author(name='Venezuelan Bolivar',icon_url='https://cdn.urgente24.com/sites/default/files/notas/2015/05/29/maduro-risa-425x318.jpg')
        embed.add_field(name='1USD is...', value=str(price)+' Bs.F')
        embed.set_footer(text="This isn't real socialism")
        return await client.say(embed=embed)

@client.command()
async def emoji(emoji):
    emoji_id = str(emoji)[-19:]
    emoji_id = emoji_id[:-1]
    emojis = client.get_all_emojis()
    for emoji in emojis:
        if emoji.id == emoji_id:
            embed = discord.Embed(Title='Emoji')
            embed.add_field(name='Emoji name', value=emoji.name,inline=False)
            embed.add_field(name='Emoji ID', value=str(emoji.id),inline=False)
            url = "https://media.discordapp.net/emojis/{}".format(emoji.id)
            print(url)
            embed.set_image(url=url)
            return await client.say(embed=embed)

@client.command(pass_context=True)
async def ping(ctx):
	t1 = time.perf_counter()
	await client.send_typing(ctx.message.channel)
	t2 = time.perf_counter()
	return await client.say('I work!!! `{}ms`'.format(int( float("%.2f"%(t2-t1))*100)))

@client.command(pass_context=True)
async def hastebin(ctx):
    await client.say(':pencil: Enter your paste in a triple-backtick code-block or type `cancel` to cancel.')
    msg = await client.wait_for_message(timeout=300,author=ctx.message.author,channel=ctx.message.channel)
    if msg.content == 'cancel':
        return await client.say(':x: Cancelled...')
    if msg == None:
        return await client.say(':zzz: Timed out...') 
    msg_txt = msg.content[3:-3]
    async with aiohttp.post("https://hastebin.com/documents",data=msg_txt.encode('utf-8')) as post:
        post = await post.json()
        url = "https://hastebin.com/{}".format(post['key']) 
    embed = discord.Embed(title="Paste created successfully!",color=0x424ef4)
    embed.set_author(name=url,url=url)
    await client.say(embed=embed)
    return await client.delete_message(msg)

@client.command()
async def shibe():
	async with aiohttp.get("http://shibe.online/api/shibes?count=10&urls=true&httpsUrls=false") as shibe:
		shibe = await shibe.json()
		embed = discord.Embed(title="Shibeeee")
		embed.set_image(url=random.choice(shibe))
		return await client.say(embed=embed)

@client.command()
async def cat():
    async with aiohttp.get("https://aws.random.cat/meow") as cat:
        cat = await cat.json()
        embed = discord.Embed(title="Catoooo")
        embed.set_image(url=cat['file'])
        return await client.say(embed=embed)

@client.command()
async def mcafee(bpi=None):
    if not bpi:
        coin_json = await aiohttp.get('https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD,EUR')
        coin_json = await coin_json.json()
        bpi = coin_json['USD']
    else:
        bpi = int(bpi)
    tbpi = 2244.265
    days_elapsed = (datetime.now()-datetime.strptime('07 17 17','%m %d %y')).days
    days_left = (datetime.strptime('12 31 20','%m %d %y')-datetime.now()).days
    grate = 0.7826319559
    pprice = 10**(grate*(days_elapsed/365))*tbpi
    pdiff = ((bpi-pprice)/pprice)*100
    pprice = "%.2f" % pprice
    aheadOrBelowStr = "ahead of"
    droppedOrIncreasedStr = 'If the price dropped to ${} it would still be'.format(pprice)
    if pdiff in range(0,10):
        isdickonthemenu = "Maybe?"
        thmb = "http://i0.kym-cdn.com/photos/images/masonry/001/062/427/2f7.jpg"
        emcolor = 0xf2c307
    elif pdiff>10:
        isdickonthemenu = "No!"
        thmb = "https://i.warosu.org/data/biz/img/0096/98/1527820986778.png"
        emcolor = 0x099b0b
    else:
        aheadOrBelowStr = "below"
        isdickonthemenu = "Yes!!!"
        thmb = "https://image.jimcdn.com/app/cms/image/transf/dimension=372x10000:format=png/path/sb4e45334ca2daabf/image/i3b0c19a39abe4003/version/1526826369/image.png"
        droppedOrIncreasedStr = 'The price needs to increase to ${} to be'.format(pprice)
        emcolor = 0xe00808
    pdiff = "%.2f" % pdiff    
    embed = discord.Embed(Title=isdickonthemenu, color=emcolor)
    embed.set_author(name="Will McAfee eat his own dick ? {}".format(isdickonthemenu))
    embed.add_field(name="The current Bitcoin price is **${}**".format(bpi),value="**{}%** {} McAfee's bet's price target".format(pdiff,aheadOrBelowStr))
    embed.add_field(name=droppedOrIncreasedStr,value="on target for $1M/Bitcoin by the three year deadline ending in **{} days**".format(days_left))
    embed.set_image(url="https://diegorod.github.io/WillMcAfeeEatHisOwnDick/img/tweet2.jpg")
    embed.set_thumbnail(url=thmb)
    return await client.say(embed=embed)

play = {"user":"","play":""}
usrs = {}
@client.group(pass_context=True)
async def playing(ctx):
    if not ctx.invoked_subcommand:
        if len(play["play"])>0:
            usr = await client.get_user_info(play["user"])
            e = discord.Embed(name="Currently playing...")
            e.set_author(name=play["play"])
            e.set_footer(text="Submitted by: {}".format(str(usr)))
            return await client.say(embed=e)
        else:
            return await client.say("Not playing anything ¯\_(ツ)_/¯")

@playing.command(pass_context=True)
async def submit(ctx,*name):
    if ctx.message.author.id in usrs:
        tm = usrs[ctx.message.author.id] - time.time()
        if tm<86400:
            return await client.say(":negative_squared_cross_mark:  You need to wait **{}** before you can submit a new status".format(time.strftime('%H:%M:%S', time.gmtime(tm))))
    name = " ".join(name)
    if len(name)>30:
        return await client.say("Your game title can't be longer than 30 characters")
    await db.insert(table="playing_status",values={"usr_id":ctx.message.author.id,"title":ascii_convert(name)})
    usrs[ctx.message.author.id] = time.time()
    play["user"] = ctx.message.author.id
    play["play"] = ascii_convert(name)
    await client.change_presence(game=discord.Game(name=name))
    return await client.say(":white_check_mark: Your playing status has been submitted!")

async def update_playing():
    await client.wait_until_ready()
    while not client.is_closed:
        await db.db.execute("SELECT usr_id,title FROM playing_status ORDER BY RANDOM() LIMIT 1")
        res = await db.db.fetchone()
        if res:
            play["user"] = res[0]
            play["play"] = res[1]
            await client.change_presence(game=discord.Game(name=res[1]))
        await asyncio.sleep(600)
client.loop.create_task(update_playing())

@client.command()
async def btx():
    async with json.loads(open("/misc/verbs.json","r").read()) as f:
        x = random.choice(f)
        y = random.choice(f)
        if x!=y:
            return client.say("Born to {} forced to {}".format(x,y))
        return client.say("You lose")