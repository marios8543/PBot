from pbot_utils import *
from modules.jikanpy import jikan

api = jikan.Jikan()


@client.group(pass_context=True)
async def anime(ctx):
	if ctx.invoked_subcommand == None:
		return await client.say(":negative_squared_cross_mark: Valid parameters are `search` and `top`")

@anime.command(pass_context=True)
async def search(ctx,*args):
	query = ' '.join(args)
	await client.send_typing(ctx.message.channel)
	result = await api.search('anime',query)
	embed = discord.Embed(title="\u200b")
	embed.set_author(name="Anime Search Result",icon_url="https://c.wallhere.com/photos/c1/a7/anime_anime_girls_Senjougahara_Hitagi_Monogatari_Series_hat-58159.jpg!d")
	embed.set_footer(text="Enter the number you want or cancel to exit")
	idx = 0
	for show in result['result']:
		idx = idx+1
		embed.add_field(name='{}. {}'.format(idx,show['title']),value="\u200b",inline=False)
	srch_msg = await client.say(embed=embed)
	msg = await client.wait_for_message(timeout=120,author=ctx.message.author,channel=ctx.message.channel)
	if msg.content=='cancel':
		return await client.say(':x: Cancelled')
	if msg==None:
		return await client.say(':zzz: Timed out')
	if int(msg.content)>len(result['result']):
		return await client.say(':negative_squared_cross_mark: Could not find that number')
	await client.send_typing(ctx.message.channel)	
	anime = await api.anime(result['result'][int(msg.content)-1]['mal_id'])
	embed = discord.Embed(title="Anime Search Result")
	embed.set_author(name="{} ({})".format(anime['title'],anime['title_japanese']),icon_url=anime['image_url'],url=anime['link_canonical'])
	embed.set_thumbnail(url=anime['image_url'])
	embed.add_field(name="Episode Count",value=anime['episodes'],inline=True)
	embed.add_field(name="Status",value=anime['status'],inline=True)
	embed.add_field(name="Score",value=anime['score'],inline=True)
	embed.add_field(name="Ranking",value=anime['rank'],inline=True)
	embed.add_field(name="Popularity",value=anime['popularity'],inline=True)
	embed.add_field(name="Synopsis",value=anime['synopsis'][:1020]+'...',inline=False)
	embed.set_footer(text="Aired from {} to {}".format(anime['aired']['from'],anime['aired']['to']))
	await client.delete_message(srch_msg)
	return await client.say(embed=embed)

@anime.command(pass_context=True)
async def top(ctx,arg):
	if arg not in ['upcoming','tv','movie','airing','ova','special']:
		return await client.say(":negative_squared_cross_mark: Valid arguments are `tv`,`movie`,`ova`,`special`,`upcoming`,`airing`")
	await client.send_typing(ctx.message.channel)	
	result = await api.top(arg)
	embed = discord.Embed(title="Top {} anime".format(arg))
	idx = 0
	for anime in result['top']:
		idx = idx+1
		embed.add_field(name="{}. {}".format(idx,anime['title']),value="Score: {}   Season: {}   Episode Count: {}".format(anime['score'],anime['airing_start'],anime['episodes']))
	embed.set_footer(text="Enter the number you want or cancel to exit")
	srch_msg = await client.say(embed=embed)
	msg = await client.wait_for_message(timeout=120,author=ctx.message.author,channel=ctx.message.channel)
	if msg.content=='cancel':
		return await client.say(':x: Cancelled')
	if msg==None:
		return await client.say(':zzz: Timed out')
	if int(msg.content)>len(result['top']):
		return await client.say(':negative_squared_cross_mark: Could not find that number')
	await client.send_typing(ctx.message.channel)	
	anime = await api.anime(result['top'][int(msg.content)-1]['mal_id'])
	embed = discord.Embed(title="Anime Search Result")
	embed.set_author(name="{} ({})".format(anime['title'],anime['title_japanese']),icon_url=anime['image_url'],url=anime['link_canonical'])
	embed.set_thumbnail(url=anime['image_url'])
	embed.add_field(name="Episode Count",value=anime['episodes'],inline=True)
	embed.add_field(name="Status",value=anime['status'],inline=True)
	embed.add_field(name="Score",value=anime['score'],inline=True)
	embed.add_field(name="Ranking",value=anime['rank'],inline=True)
	embed.add_field(name="Popularity",value=anime['popularity'],inline=True)
	embed.add_field(name="Synopsis",value=anime['synopsis'][:1020]+'...',inline=False)
	embed.set_footer(text="Aired from {} to {}".format(anime['aired']['from'],anime['aired']['to']))
	await client.delete_message(srch_msg)
	return await client.say(embed=embed)



	




