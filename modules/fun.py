from pbot_utils import *
import xml.etree.ElementTree as xml
import random
import aiohttp
from time import strptime

session = aiohttp.ClientSession()

@client.command()
async def bsf():
    async with session.get('https://s3.amazonaws.com/dolartoday/data.json')as dolartoday:
        result = await dolartoday.json(encoding='cp1252')
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
    emojis = client.get_all_emojis()
    for emoji in emojis:
        if emoji.id == emoji_id:
            embed = discord.Embed(Title='Emoji')
            embed.add_field(name='Emoji name', value=emoji.name,inline=False)
            embed.add_field(name='Emoji ID', value=str(emoji.id),inline=False)
            url = emoji.url
            print(url)
            embed.set_image(url=url)
            await client.say(embed=embed)

@client.command()
async def ping():
    timestamp = datetime.now()
    msg = await client.say('I work!!!')
    msg_time = msg.timestamp
    result = timestamp - msg_time
    result = result.total_seconds()
    await client.edit_message(msg,'I work!!! `'+str(abs(result))[:-3]+'sec`')

@client.command(pass_context=True)
async def rule34(ctx,tag):
    if 'nsfw' not in ctx.message.channel.name:
        return await client.say(":negative_squared_cross_mark: You can only use this in NSFW channels")  
    async with session.get('https://rule34.xxx/index.php?page=dapi&s=post&q=index&limit=50&tags={}'.format(tag)) as result:
        result = await result.text()
        result = xml.fromstring(result.encode())
        if len(result)==0:
            return await client.say(":red_circle: Couldn't find anything on that")
        post = random.choice(result).attrib
        embed = discord.Embed(Title='Rule34')
        embed.set_author(icon_url='https://image.ibb.co/dFAmGT/r34.png',url='https://rule34.xxx/index.php?page=post&s=view&id={}'.format(post['id']),name='ID: {}'.format(post['id']))
        embed.add_field(name='Rating',value=post['rating'].upper())
        embed.add_field(name='Score',value=post['score'])
        embed.set_image(url=post['file_url'])
        stm = post['created_at'].split(' ')
        embed.set_footer(text='Created at {}/{}/{}'.format(stm[2],strptime(stm[1],'%b').tm_mon,stm[-1]))
        return await client.say(embed=embed)

@client.command(pass_context=True)
async def hastebin(ctx):
    await client.say(':pencil: Enter your paste in a triple-backtick code-block or type `cancel` to cancel.')
    msg = await client.wait_for_message(timeout=300,author=ctx.message.author,channel=ctx.message.channel)
    if msg.content == 'cancel':
        return await client.say(':x: Cancelled...')
    if msg == None:
        return await client.say(':zzz: Timed out...') 
    msg_txt = msg.content[3:-3]
    async with session.post("https://hastebin.com/documents",data=msg_txt.encode('utf-8')) as post:
        post = await post.json()
        url = "https://hastebin.com/{}".format(post['key']) 
    embed = discord.Embed(title="Paste created successfully!",color=0x424ef4)
    embed.set_author(name=url,url=url)
    await client.say(embed=embed)
    return await client.delete_message(msg)
