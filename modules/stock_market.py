from pbot_utils import client,config
from time import mktime
from datetime import datetime
from io import BytesIO
import matplotlib.pyplot as plt
import aiohttp
import discord
import os

BASE_URL = "https://www.alphavantage.co/query"
if os.getenv("SM_API_KEY"):
    API_KEY = os.getenv("SM_API_KEY")
elif "sm_api_key" in config:
    API_KEY = config["sm_api_key"]
else:
    API_KEY=None
intervals=[1,5,15,30,60]
plt.rcParams["figure.figsize"] = (5,1)

def getunixtime(k):
    try:
        tm = datetime.strptime(k,"%Y-%m-%d %H:%M:%S")
    except ValueError:
        try:
            tm = datetime.strptime(k,"%Y-%m-%d")
        except ValueError:
            return "https://cdn.discordapp.com/attachments/444563563953127427/515859490499854346/ERROR.png"
    return mktime(tm.timetuple())

async def plot(data):
    sio = BytesIO()
    sio.name = "plot.png"
    xdata = [getunixtime(k) for k,v in data]
    ydata = [float(v['1. open']) for k,v in data]
    plt.clf()
    plt.plot(xdata,ydata)
    fig = plt.gcf()
    fig.savefig(sio,format='png')
    sio.seek(0)
    msg = await client.send_file(client.get_channel('515844409905119262'),sio)
    return msg.attachments[0]['url']

async def base_call(ctx,sym,ival,func):
    ival = ival if ival in intervals else 15
    if not API_KEY:
        return await client.say("Service inactive")
    if not sym or sym=="":
        return await client.say(":negative_squared_cross_mark: No symbol specified")
    await client.send_typing(ctx.message.channel)
    sym = sym.upper()
    async with aiohttp.get(BASE_URL,params={'function':func,'symbol':sym,'interval':str(ival)+'min' if ival else None,'apikey':API_KEY}) as r:
        r = await r.json()
        if not "Error Message" in r:
            d = list(r[list(r)[1]].items())
            e = discord.Embed()
            e.set_author(name="{} for symbol {}".format(r['Meta Data']['1. Information'],r['Meta Data']['2. Symbol']))
            e.add_field(name="Timestamp",value=d[0][0],inline=False)
            e.add_field(name="Open  -  Close",value="${}  -  ${}".format(d[0][1]['1. open'],d[0][1]['4. close']))
            e.add_field(name="High  -  Low",value="${}  -  ${}".format(d[0][1]['2. high'],d[0][1]['3. low']))
            e.set_footer(text="Last refreshed on {}".format(r['Meta Data']['3. Last Refreshed']))
            e.set_image(url=await plot(d))
            return await client.say(embed=e)
        else:
            return await client.say(":negative_squared_cross_mark: {}".format(r['Error Message']))

@client.group(pass_context=True,invoke_without_command=True)
async def stock(ctx,sym:str=None,ival=15):
    if not ctx.invoked_subcommand:
        await ctx.invoke(intraday,sym=sym,ival=ival)

@stock.command(pass_context=True)
async def intraday(ctx,sym,ival=15):
    return await base_call(ctx,sym,None,'TIME_SERIES_INTRADAY')

@stock.command(pass_context=True)
async def daily(ctx,sym):
    return await base_call(ctx,sym,None,'TIME_SERIES_DAILY')

@stock.command(pass_context=True)
async def weekly(ctx,sym):
    return await base_call(ctx,sym,None,'TIME_SERIES_WEEKLY')

@stock.command(pass_context=True)
async def monthly(ctx,sym):
    return await base_call(ctx,sym,None,'TIME_SERIES_MONTHLY')