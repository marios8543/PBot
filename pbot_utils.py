import json
import time
import discord
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands
import unicodedata
from datetime import datetime
from random import randint
import hashlib
import pbot_orm

#Parse config
with open("config.json","r+") as config:
    config = json.loads(config.read())    

def timestamp():
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return timestamp

async def log_members():
    res = await db.selectmany(table='members',fields=['id','server_id'])
    res2 = set(client.get_all_members())
    members = []
    db_members = []
    for r in res:
        db_members.append((r.id,r.server_id))
    for r in res2:
        members.append((int(r.id),int(r.server.id)))
    missing = set(members)-set(db_members)
    for m in missing:
        await db.insert(table='members',values={'id':m[0],'server_id':m[1],'verified':1})
        print('Saved missing member {} (ServerID: {})'.format(m[0],m[1]))
    return 1

async def log_servers():
    res = await db.selectmany(table='servers',fields=['id'])
    db_servers = [r.id for r in res]
    servers = [int(s.id) for s in client.servers]
    missing = set(servers) - set(db_servers)
    for m in missing:
        await Utils.make_server(id=m)
        print("Logged missing server ",m)
    return 1    



client = Bot(description="pbot_public", command_prefix=">>")
warn_whitelist = config['warn_whitelist']
logging_blacklist = []
db = pbot_orm.ORM(None,None)


@client.event
async def on_ready():
    dicc = await pbot_orm.connect(database=config['database'],loop=client.loop)
    db.db = dicc['db']
    db.conn = dicc['conn']
    await log_servers()
    await log_members()
    logging_blacklist.append(config['logging_blacklist'])
    logging_blacklist.append(client.user.id)
    print('Logged in as '+client.user.name+' (ID:'+client.user.id+') | Connected to '+str(len(client.servers))+' servers | Connected to '+str(len(set(client.get_all_members())))+' users')

def ascii_convert(s):
    if type(s)==str:
        return unicodedata.normalize('NFKD', s).encode('ascii','ignore')
    else:
        return s    


class User():
    id = ""
    name = ""
    server_id = ""
    join_date = ""
    info = ""
    warnings = 0
    verified = 0
    present = 0

    def __init__(self,id,server_id,warnings,verified,present):
        self.id = id
        self.server_id = server_id
        self.warnings = warnings
        self.present = present
        self.disc_user = client.get_server(self.server_id).get_member(id)
        self.name = self.disc_user.name+'#'+self.disc_user.discriminator
        self.join_date = self.disc_user.joined_at
        

    async def update(self):
        update_dic = {
            'warns':self.warnings,
            'verified':self.verified,
            'in_server':self.present
        }
        await db.update(table='members',values=update_dic,params={'id':self.id,'server_id':self.server_id})
        return 1

    async def warn(self):
        if self.warnings+1 >= self.server.max_warnings:
                return 2
        else:
            self.warnings = self.warnings+1
            await self.update()
            return 1

class Server():
    id = ""
    name=""
    added_on = ""
    welcome_channel = ""
    goodbye_channel = ""
    event_channel = ""
    log_channel = ""
    log_active = 0
    log_whitelist = []
    entry_text = ""
    entry_text_pm = ""
    goodbye_text = ""
    max_warnings = 0

    async def update(self):
        if self.log_whitelist!=0:
            log_whitelist = json.dumps(self.log_whitelist)
        else:
            log_whitelist=0          
        update_dic = {
            'welcome_channel':self.welcome_channel,
            'goodbye_channel':self.goodbye_channel,
            'event_channel':self.event_channel,
            'log_channel':self.log_channel,
            'log_active':json.dumps(self.log_active),
            'log_whitelist':log_whitelist,
            'entry_text':ascii_convert(self.entry_text),
            'entry_text_pm':ascii_convert(self.entry_text_pm),
            'goodbye_text':ascii_convert(self.goodbye_text),
            'max_warns':self.max_warnings
        }
        #print(update_dic)
        await db.update(table='servers',values=update_dic,params={'id':str(self.id)})
        return 1

    async def get_member(self,id):
        res = await db.select(table='members',fields=[
            'warns','verified',
            'in_server'],params={'server_id':self.id,
            'id':id})
        if res:
            user = User(id,self.id,res.warns,res.verified,res.in_server)
            user.server = await Utils.get_server(self.id)
            return user

    async def make_member(self,id,verified=0):
        await db.insert(table='members',values={
            'id':id,
            'server_id':self.id,
            'verified':verified
            })
        return await self.get_member(id)

    async def toggle_logging_msg(self):
        if self.log_active['msg']==0:
            self.log_active['msg']=1
            if await self.update():
                return 1              
        else:
            self.log_active['msg']=0
            if await self.update():
                return 2

    async def toggle_logging_name(self):
        if self.log_active['name']==0:
            self.log_active['name']=1
            if await self.update():
                return 1              
        else:
            self.log_active['name']=0
            if await self.update():
                return 2                

class Utils():

    async def get_server(id):
        result = await db.select(table='servers',fields=[
        'added_on','entry_text','entry_text_pm','goodbye_text',
        'log_whitelist','welcome_channel','goodbye_channel','event_channel',
        'log_channel','log_active','max_warns'],params={'id':id})
        id = str(id)
        if result==None:
            return
        if result.log_whitelist:
            log_whitelist = json.loads(result.log_whitelist)
        else:
            log_whitelist=0
        if result.entry_text==None:
            result.entry_text = config['default_entrytext']
        if result.entry_text_pm==None:
            result.entry_text_pm = config['default_entrytextpm']
        if result.goodbye_text==None:
            result.goodbye_text = config['default_goodbye']
        srv = Server()          
        srv.id = id
        srv.added_on = result.added_on
        srv.welcome_channel = result.welcome_channel
        srv.goodbye_channel = result.goodbye_channel
        srv.event_channel = result.event_channel
        srv.log_channel = result.log_channel
        srv.log_active = json.loads(result.log_active)
        srv.log_whitelist = log_whitelist
        srv.entry_text = result.entry_text
        srv.entry_text_pm = result.entry_text_pm
        srv.goodbye_text = result.goodbye_text
        srv.max_warnings = int(result.max_warns)
        srv.disc_server = client.get_server(id)
        return srv

    def random(dig):
        size = "0"
        while len(size)<=dig:
            size = size+'0'
        return randint(int('1'+size),int('1'+size+'0'))

    def make_hash(*args,length=64):
        tobehashed = ''
        for arg in args:
            tobehashed = tobehashed+str(arg)
        tobehashed = tobehashed.encode("utf-8")
        hash_object = hashlib.sha256(tobehashed)
        return hash_object.hexdigest()[:length]    

    def check_perms_ctx(ctx,perm):
        server = ctx.message.server
        user = server.get_member(ctx.message.author.id)
        return getattr(user.server_permissions,perm)
        
    async def make_server(id=0):
        await db.insert(table='servers',values={'id':id})
        return await Utils.get_server(id)
                        
    async def delete_server(id):
        await db.delete(table='servers',params={'id':id})
        await db.delete(table='members',params={'server_id':id})
