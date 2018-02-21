#Returns info and big version of an emoji (Only custom emojis)
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


#Gets the price of the Venezuelan Bolivar
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
