from pbot_utils import *
import aiohttp

@client.group(pass_context=True)
async def crypto(ctx):
    if ctx.invoked_subcommand is None:
        await client.say('Invalid subcommand')

#Bitcoin price
@crypto.command()
async def btc():
	async with aiohttp.get('https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD,EUR') as coin_json:
		result_stats = await coin_json.json()
		usdprice = result_stats['USD']
		eurprice = result_stats['EUR']
		embed=discord.Embed(title='The current bitcoin price is:', color=0xf3c405)
		embed.set_author(name='Bitcoin',icon_url='https://cdn.pixabay.com/photo/2013/12/08/12/12/bitcoin-225079_960_720.png')
		embed.add_field(name='USD', value=str(usdprice)+'$', inline=False)
		embed.add_field(name='EUR', value=str(eurprice)+'€', inline=False)
		embed.set_footer(text="KryptoBot")
		await client.say(embed=embed)

#Ethereum price
@crypto.command()
async def eth():
	async with aiohttp.get('https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD,EUR') as coin_json:
		result_stats = await coin_json.json()
		usdprice = result_stats['USD']
		eurprice = result_stats['EUR']
		embed=discord.Embed(title='The current ethereum price is:', color=0x47e463)
		embed.set_author(name='Ethereum',icon_url='https://cdn.discordapp.com/attachments/271256875205525504/374282740218200064/2000px-Ethereum_logo.png')
		embed.add_field(name='USD', value=str(usdprice)+'$', inline=False)
		embed.add_field(name='EUR', value=str(eurprice)+'€', inline=False)
		embed.set_footer(text="KryptoBot")
		await client.say(embed=embed)

#Zcash price
@crypto.command()
async def zec():
	async with aiohttp.get('https://min-api.cryptocompare.com/data/price?fsym=ZEC&tsyms=USD,EUR') as coin_json:
		result_stats = await coin_json.json()
		usdprice = result_stats['USD']
		eurprice = result_stats['EUR']
		embed=discord.Embed(title='The current zcash price is:', color=0xffad33)
		embed.set_author(name='Zcash',icon_url='https://www.zcashcommunity.com/wp-content/uploads/2017/01/cropped-yellow-zcash-logo.png')
		embed.add_field(name='USD', value=str(usdprice)+'$', inline=False)
		embed.add_field(name='EUR', value=str(eurprice)+'€', inline=False)
		embed.set_footer(text="KryptoBot")
		await client.say(embed=embed)

#Decred price
@crypto.command()
async def dcr():
	async with aiohttp.get('https://min-api.cryptocompare.com/data/price?fsym=DCR&tsyms=USD,EUR') as coin_json:
		result_stats = await coin_json.json()
		usdprice = result_stats['USD']
		eurprice = result_stats['EUR']
		embed=discord.Embed(title='The current decred price is:', color=0x47d147)
		embed.set_author(name='Decred',icon_url='https://forum.decred.org/styles/material/uix/logo.png')
		embed.add_field(name='USD', value=str(usdprice)+'$', inline=False)
		embed.add_field(name='EUR', value=str(eurprice)+'€', inline=False)
		embed.set_footer(text="KryptoBot")
		await client.say(embed=embed)

#Dash price
@crypto.command()
async def dash():
	async with aiohttp.get('https://min-api.cryptocompare.com/data/price?fsym=DASH&tsyms=USD,EUR') as coin_json:
		result_stats = await coin_json.json()
		usdprice = result_stats['USD']
		eurprice = result_stats['EUR']
		embed=discord.Embed(title='The current dash price is:', color=0x0080ff)
		embed.set_author(name='Dash',icon_url='http://bitcoinchaser.com/wp-content/uploads/2017/03/dashcoin-300x300.png')
		embed.add_field(name='USD', value=str(usdprice)+'$', inline=False)
		embed.add_field(name='EUR', value=str(eurprice)+'€', inline=False)
		embed.set_footer(text="KryptoBot")
		await client.say(embed=embed)

#Litecoin price
@crypto.command()
async def ltc():
	async with aiohttp.get('https://min-api.cryptocompare.com/data/price?fsym=LTC&tsyms=USD,EUR') as coin_json:
		result_stats = await coin_json.json()
		usdprice = result_stats['USD']
		eurprice = result_stats['EUR']
		embed=discord.Embed(title='The current litecoin price is:', color=0xC8C8C8)
		embed.set_author(name='Litecoin',icon_url='http://ltc.133.io/images/logosizes/ltc800.png')
		embed.add_field(name='USD', value=str(usdprice)+'$', inline=False)
		embed.add_field(name='EUR', value=str(eurprice)+'€', inline=False)
		embed.set_footer(text="KryptoBot")
		await client.say(embed=embed)

#Ripple price
@crypto.command()
async def xrp():
	async with aiohttp.get('https://min-api.cryptocompare.com/data/price?fsym=XRP&tsyms=USD,EUR') as coin_json:
		result_stats = await coin_json.json()
		usdprice = result_stats['USD']
		eurprice = result_stats['EUR']
		embed=discord.Embed(title='The current ripple price is:', color=0x1a53ff)
		embed.set_author(name='Ripple',icon_url='http://bitcoinist.com/wp-content/uploads/2016/08/Ripple-logo.png')
		embed.add_field(name='USD', value=str(usdprice)+'$', inline=False)
		embed.add_field(name='EUR', value=str(eurprice)+'€', inline=False)
		embed.set_footer(text="KryptoBot")
		await client.say(embed=embed)

#Ethereum classic price
@crypto.command()
async def etc():
	async with aiohttp.get('https://min-api.cryptocompare.com/data/price?fsym=ETC&tsyms=USD,EUR') as coin_json:
		result_stats = await coin_json.json()
		usdprice = result_stats['USD']
		eurprice = result_stats['EUR']
		embed=discord.Embed(title='The current ethereum classic price is:', color=0x33cc33)
		embed.set_author(name='Ethereum Classic',icon_url='https://raw.githubusercontent.com/ethereumclassic/Media_Kit/master/Classic_Logo_Solid/ETC_LOGO_Full_Color_Green.png')
		embed.add_field(name='USD', value=str(usdprice)+'$', inline=False)
		embed.add_field(name='EUR', value=str(eurprice)+'€', inline=False)
		embed.set_footer(text="KryptoBot")
		await client.say(embed=embed)

#Dogecoin price
@crypto.command()
async def doge():
	async with aiohttp.get('https://min-api.cryptocompare.com/data/price?fsym=DOGE&tsyms=USD,EUR') as coin_json:
		result_stats = await coin_json.json()
		usdprice = result_stats['USD']
		eurprice = result_stats['EUR']
		embed=discord.Embed(title='The current dogecoin price is:', color=0xcc9900)
		embed.set_author(name='Dogecoin',icon_url='https://i.redd.it/ony3qesa3ebx.png')
		embed.add_field(name='USD', value=str(usdprice)+'$', inline=False)
		embed.add_field(name='EUR', value=str(eurprice)+'€', inline=False)
		embed.set_footer(text="KryptoBot")
		await client.say(embed=embed)

#Bitcoin cash prices
@crypto.command()
async def bch():
	async with aiohttp.get('https://min-api.cryptocompare.com/data/price?fsym=BCH&tsyms=USD,EUR') as coin_json:
		result_stats = await coin_json.json()
		usdprice = result_stats['USD']
		eurprice = result_stats['EUR']
		embed=discord.Embed(title='The current bitcoin cash price is:', color=0xf3c405)
		embed.set_author(name='Bitcoin Cash',icon_url='https://files.coinmarketcap.com/static/img/coins/32x32/bitcoin-cash.png')
		embed.add_field(name='USD', value=str(usdprice)+'$', inline=False)
		embed.add_field(name='EUR', value=str(eurprice)+'€', inline=False)
		embed.set_footer(text="KryptoBot")
		await client.say(embed=embed)