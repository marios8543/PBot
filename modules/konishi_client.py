from pbot_utils import *
import aiohttp
import json
h = {'Content-type':'application/json'}

try:
	BASE_URL = config['konishi_url']
except:
	BASE_URL = None

async def handle_image(msg):
	if len(msg.attachments)>0:
		img = msg.attachments[0]
		async with aiohttp.get(img['url']) as r:
			r = await r.read()
			return {'data':r,'name':img['filename']}
	return

@client.group(pass_context=True)
async def konishi(ctx):
	if not ctx.message.channel.is_private:
		return await client.say(":negative_squared_cross_mark: You can only use Konishi in PM")
	if not BASE_URL or BASE_URL=="":
		return await client.say(":negative_squared_cross_mark: Konishi not implemented")
	if not ctx.invoked_subcommand:
		return await client.say(":negative_squared_cross_mark: Bad command")

@konishi.command(pass_context=True)
async def login(ctx):
	creds={"username":"","password":""}
	await client.say("""
		Logging into Konishi through >PBot will bind your account to your Discord ID
		If you agree proceed or else type `cancel`...""")
	for i in creds:
		await client.say("Enter your {}".format(i))
		msg = await client.wait_for_message(author=ctx.message.author,channel=ctx.message.channel,timeout=120)
		if msg==None or 'cancel' in msg.content:
			return await client.say(":zzz: Cancelled...")
		creds[i]=msg.content
	await client.send_typing(ctx.message.channel)
	async with aiohttp.post("{}/login".format(BASE_URL),data=json.dumps(creds),headers=h) as resp:
		r = await resp.json()
		if resp.status==200:
			await client.say(""":white_check_mark: Login successfull!
			Please delete your password for safety reasons""")
			return await db.update(table='members',values={'konishi':r['access_token']},params={'id':ctx.message.author.id})
		else:
			return await client.say(":negative_squared_cross_mark: {}".format(r['message']))

@konishi.command(pass_context=True)
async def post(ctx):
	tkn = await db.select(table='members',fields=['konishi'],params={'id':ctx.message.author.id})
	if not tkn:
		return await client.say(":negative_squared_cross_mark: Not logged in...")
	else:
		tkn = tkn.konishi
	await client.say(":pencil: Write your post. You can also include an image...")
	msg = await client.wait_for_message(author=ctx.message.author,channel=ctx.message.channel,timeout=300)
	if not msg:
		return await client.say(":negative_squared_cross_mark: Cancelled...")
	content = msg.content
	img = await handle_image(msg)
	if img:
		data = aiohttp.FormData()
		data.add_field('file',img['data'],filename=img['name'])
		async with aiohttp.post("{}/imageupload".format(BASE_URL),data=data,headers={'Authorization':'Bearer '+tkn}) as resp:
			if resp.status==200:
				r = await resp.json()
				img = r['image_id']
			else:
				t = await resp.text()
				return await client.say(":negative_squared_cross_mark: Image upload error: {}".format(t))
	async with aiohttp.post("{}/posts".format(BASE_URL),data=json.dumps({'content':content,'image_id':img}),headers={'Authorization':'Bearer '+tkn,'Content-type':'application/json'}) as resp:
		r = await resp.json()
		if '2' in str(resp.status):
			return await client.say(":white_check_mark: Post created successfully!")
		else:
			return await client.say(":negative_squared_cross_mark: Error: {}".format(r['message']))

usr={}
@konishi.command(pass_context=True)
async def feed(ctx):
	tkn = await db.select(table='members',fields=['konishi'],params={'id':ctx.message.author.id})
	if not tkn:
		return await client.say(":negative_squared_cross_mark: Not logged in...")
	else:
		tkn = tkn.konishi
	if ctx.message.author in usr:
		for m in usr[ctx.message.author]:
			await client.delete_message(m['message'])
		usr[ctx.message.author]=[]
	else:
		usr[ctx.message.author]=[]
	async with aiohttp.get("{}/feed".format(BASE_URL),params={'limit':10},headers={'Authorization':'Bearer '+tkn}) as resp:
		if resp.status==200:
			r = await resp.text()
			async with aiohttp.post("{}/feed".format(BASE_URL),data=r,headers=({'Content-type':'application/json','Authorization':'Bearer '+tkn})) as r:
				if r.status==200:
					r = await r.json()
					for r in r['posts']:
						embed = discord.Embed()
						embed.set_author(name=r['creator_name'])
						embed.description = r['content']
						embed.add_field(name="{} Likes".format(len(r['likes'])),value="{} Comments".format(len(r['comments'])),inline=True)
						embed.set_footer(text="Created at {}".format(r['created']))
						m = await client.say(embed=embed)
						await client.add_reaction(m,'\U0001f44d')
						if len(r['comments'])>0:
							await client.add_reaction(m,'\U0001f5e8')
						await client.add_reaction(m,'\U0000270f')
						usr[ctx.message.author].append({'message':m,'post':r['id'],'embed':embed})
				else:
					r = await r.json()
					await client.say(":negative_squared_cross_mark: Error: {}".format(r['message']))
		else:
			resp = await resp.json()
			await client.say(":negative_squared_cross_mark: Error: {}".format(resp['message']))
	return

@client.listen('on_reaction_add')
async def reactionadd(r,u):
	if u==client.user:
		return
	if str(r.message.id) in [r['message'].id for r in usr[u]]:
		tkn = await db.select(table='members',fields=['konishi'],params={'id':u.id})
		if not tkn:
			return
		else:
			tkn = tkn.konishi
		p = None
		for i in usr[u]:
			if i['message'].id==r.message.id:
				p = i['post']
				m = i['message']
				e = i['embed']
				break
		if not p:
			return
		if r.emoji == '\U0001f44d':
			async with aiohttp.post("{}/post/{}/like".format(BASE_URL,p),headers={'Authorization':'Bearer '+tkn}) as resp:
				if resp.status==201:
					await client.send_message(u,":white_check_mark: You liked a post!")
				else:
					resp = await resp.json()
					await client.send_message(u,":negative_squared_cross_mark: Error: {}".format(resp['message']))
		elif r.emoji == '\U0000270f':
			await client.send_message(u,":pencil: Write your reply. You can also include an image...")
			while True:
				msg = await client.wait_for_message(author=u,channel=None,timeout=300)
				if not msg or msg.content=='cancel':
					return await client.send_message(u,":negative_squared_cross_mark: Cancelled...")
				if not msg.server:
					break
			content = msg.content
			async with aiohttp.post("{}/post/{}/comments".format(BASE_URL,p),data=json.dumps({'content':content}),headers={'Authorization':'Bearer '+tkn,'Content-type':'application/json'}) as resp:
				r = await resp.json()
				if '2' in str(resp.status):
					return await client.send_message(u,":white_check_mark: Post created successfully!")
				else:
					return await client.send_message(u,":negative_squared_cross_mark: Error: {}".format(r['message']))
		elif r.emoji == '\U0001f5e8':
			for m in [r['message'] for r in usr[u]]:
				await client.delete_message(m)
			usr[u]=[]
			e.color = 0xffffff
			await client.send_message(u,embed=e)
			async with aiohttp.get("{}/post/{}/comments".format(BASE_URL,p),headers={'Authorization':'Bearer '+tkn}) as resp:
				if resp.status==200:
					resp = await resp.json()
					for i in resp['comments']:
						embed = discord.Embed(description=i['content'])
						embed.set_author(name=i['commenter'])
						embed.add_field(name="{} Likes".format(len(i['likes'])),value="{} Comments".format(len(i['replies'])),inline=True)
						embed.set_footer(text=i['created'])
						m = await client.send_message(u,embed=embed)
						usr[ctx.message.author].append({'message':m,'post':i['id'],'embed':embed})
				else:
					resp = await resp.json()
					await client.send_messageI(u,":negative_squared_cross_mark: Error: {}".format(resp['message']))
		return



@client.command(pass_context=True)
async def die(ctx):
	if ctx.message.author.id=='196224042988994560':
		await client.say("DAD WHYYYYYYY")
		exit()