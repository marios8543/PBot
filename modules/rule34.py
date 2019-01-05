from pbot_utils import client
from time import strptime
import discord
import xml.etree.ElementTree as xml
import aiohttp
import random

rule34_comm = {}

@client.command(pass_context=True)
async def rule34(ctx,*tag):
    if ctx.message.channel.name and 'nsfw' not in ctx.message.channel.name:
        return await client.say(":negative_squared_cross_mark: You can only use this in NSFW channels")
    query = "+".join(tag)
    await client.send_typing(ctx.message.channel)
    async with aiohttp.get('https://rule34.xxx/index.php?page=dapi&s=post&q=index&limit=50&tags={}'.format(query)) as result:
        result = await result.text()
        result = xml.fromstring(result.encode())
        if len(result)==0:
            return await client.say(":red_circle: Couldn't find anything on that")
        post = random.choice(result).attrib
        embed = discord.Embed(Title='Rule34')
        embed.set_author(icon_url='https://image.ibb.co/dFAmGT/r34.png',url='https://rule34.xxx/index.php?page=post&s=view&id={}'.format(post['id']),name='ID: {}'.format(post['id']))
        embed.add_field(name='Rating',value=post['rating'].upper())
        embed.add_field(name='Score',value=post['score'])
        embed.add_field(name='Tags',value=", ".join(post['tags'].split(" ")[:10])[1:]+" and more...")
        embed.set_image(url=post['file_url'])
        stm = post['created_at'].split(' ')
        embed.set_footer(text='Created at {}/{}/{}'.format(stm[2],strptime(stm[1],'%b').tm_mon,stm[-1]))
        mes = await client.say(embed=embed)
        print(post['has_comments'])
        if(post['has_comments']=="false"):
            print("no comments")
            return
        rule34_comm[str(mes.id)] = post['id']
        await client.add_reaction(mes,"\U0001f4ac")
        return

@client.listen('on_reaction_add')
async def reactionadd(reaction,user):
    if str(reaction.message.id) not in rule34_comm or user.id==client.user.id:
        return
    post_id = rule34_comm[reaction.message.id]
    async with aiohttp.get("https://rule34.xxx/index.php?page=dapi&s=comment&q=index&post_id={}".format(post_id)) as result:
        if result.status!=200:
            return
        result = xml.fromstring(await result.text())
        if len(result)==0:
            return await client.send_message(reaction.message.channel,":red_circle: Couldn't find any comments")
        embed = discord.Embed()
        embed.set_author(icon_url='https://image.ibb.co/dFAmGT/r34.png',url='https://rule34.xxx/index.php?page=post&s=view&id={}'.format(post_id),name="\U0001f5e9 Comments for post with ID {}".format(post_id))
        for i in result:
            i = i.attrib
            embed.add_field(name="{} {}".format(i['creator'],i['created_at']),value=i['body'],inline=False)
        return await client.send_message(reaction.message.channel,embed=embed)
        
        
@client.command(pass_context=True)
async def gelbooru(ctx,*tag):
    if ctx.message.channel.name and 'nsfw' not in ctx.message.channel.name:
        return await client.say(":negative_squared_cross_mark: You can only use this in NSFW channels")
    query = "+".join(tag)
    await client.send_typing(ctx.message.channel)
    async with aiohttp.get('https://gelbooru.com/index.php?page=dapi&s=post&q=index&limit=50&json=1&tags={}'.format(query)) as result:
        result = await result.json()
        if result==None:
            return await client.say(":red_circle: Couldn't find anything on that")
        post = random.choice(result)
        embed = discord.Embed(Title='Gelbooru')
        embed.set_author(icon_url='https://gelbooru.com/favicon.png',url=post['file_url'],name='ID: {}'.format(post['id']))
        embed.add_field(name='Rating',value=post['rating'].upper())
        embed.add_field(name='Score',value=post['score'])
        embed.add_field(name='Tags',value=", ".join(post['tags'].split(" ")[:10])[1:]+" and more...")
        embed.set_image(url=post['file_url'])
        stm = post['created_at'].split(' ')
        embed.set_footer(text='Created at {}/{}/{}'.format(stm[2],strptime(stm[1],'%b').tm_mon,stm[-1]))
        return await client.say(embed=embed)

@client.command(pass_context=True)
async def rtube(ctx,*tag):
    if ctx.message.channel.name and 'nsfw' not in ctx.message.channel.name:
        return await client.say(":negative_squared_cross_mark: You can only use this in NSFW channels")
    query = "+".join(tag)
    await client.send_typing(ctx.message.channel)
    async with aiohttp.get('https://api.redtube.com/?data=redtube.Videos.searchVideos&output=json&thumbsize=all',params={'search':query}) as result:
        r = await result.json()
        if r['count']==0:
            return await client.say(":red_circle: Couldn't find anything on that")
        post = random.choice(r['videos'])['video']
        thumb = None
        tags = []
        for t in post['thumbs']:
            if t['size']=='big':
                thumb=t['src']
                break
        if not thumb:
            thumb=post['thumb']
        for t in post['tags']:
            tags.append(t['tag_name'])
        embed = discord.Embed(Title='Redtube')
        embed.set_author(icon_url='http://redtubehdfree.com/hybrid_v1/m/dynamic_i/skins/redtube/app-icon.png',url=post['url'],name=post['title'])
        embed.add_field(name='Views',value=post['views'])
        embed.add_field(name='Rating',value=post['rating'])
        embed.add_field(name='Duration',value=post['duration'])
        embed.add_field(name='Tags',value=", ".join(tags[:10])[1:])
        embed.set_image(url=thumb)
        embed.set_footer(text="Published on: {}".format(post['publish_date']))
        return await client.say(embed=embed)