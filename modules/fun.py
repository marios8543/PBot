from pbot_utils import *
import aiohttp

@client.command()
async def bsf():
    async with aiohttp.get('https://s3.amazonaws.com/dolartoday/data.json')as dolartoday:
        result = json.loads(dolartoday.decode('cp1252'))
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
 await client.edit_message(msg,'I work!!! `'+str(abs(result))+'sec`')
