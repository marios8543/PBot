from pbot_utils import client,config
from asyncio import sleep
from discord import Embed
from time import gmtime, strftime
import aiohttp

BASE_URL = "https://api.exchangeratesapi.io"
coins = {}

async def update_rates():
    while not client.is_closed:
        res = await aiohttp.get("{}/latest".format(BASE_URL),params={'base':'USD'})
        try:
            tmp = await res.json()
            coins['rates'] = tmp['rates']
            coins['base'] = tmp['base']
            coins['last_refresh'] = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        except Exception:
            pass
        await sleep(3600)
client.loop.create_task(update_rates())

@client.group(pass_context=True,invoke_without_command=True)
async def forex(ctx,coin=None,coin2=None):
    if ctx.invoked_subcommand:
        return
    if not coin:
        return await client.say(":negative_squared_cross_mark: No currencies specified")
    if '/' in coin:
        coin2 = coin.split("/")[1].upper()
        coin = coin.split("/")[0].upper()
    if not coin2:
        return await client.say(":negative_squared_cross_mark: No currencies specified")
    qty=1
    if (coin[0] or 'x').isdigit():
        qty = int("".join([i for i in coin if i.isdigit()]))
        coin = "".join([i for i in coin if i.isalpha()])
    if coin in coins['rates'] and coin2 in coins['rates']:
        r = coins['rates'][coin2]/coins['rates'][coin]
        if qty>1:
            r = r*qty
    else:
        return await client.say(":negative_squared_cross_mark: Currencies not found")
    e = Embed(description=":money_with_wings: **{}{}** is currently ***{}*** {}".format(qty,coin,"%.4f"%r,coin2))
    e.set_footer(text="Last updated: {}".format(coins['last_refresh']))
    return await client.say(embed=e)

@forex.command()
async def rates(coin="USD"):
    coin = coin.upper()
    if coin not in coins['rates']:
        return await client.say(":negative_squared_cross_mark: Currency not found")
    text=":money_with_wings: ***__1{}__***  is...\n\n".format(coin)
    for k,v in coins['rates'].items():
        if coin!=coins['base']:
            v = v/coins['rates'][coin]
        text+="**{}** {}\n".format("%.4f"%v,k)
    e = Embed(description=text)
    e.set_footer(text="Last updated: {}".format(coins['last_refresh']))
    return await client.say(embed=e)