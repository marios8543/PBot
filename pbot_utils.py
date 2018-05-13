import json
import time
import discord
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands
import unicodedata
from datetime import datetime
import mysql.connector
from random import randint
import hashlib
from pbot_orm import make_orm
from urllib.request import urlopen

#Parse config
with open("config.json","r+") as config:
    config = json.loads(config.read())

conn = mysql.connector.connect(user=config['mysql_user'], password=config['mysql_password'], host=config['mysql_address'], database=config['mysql_database'])
db = conn.cursor(buffered=True)
client = Bot(description="pbot_public", command_prefix=">>")
db = make_orm(db=db,conn=conn)
warn_whitelist = config['warn_whitelist']
logging_blacklist = []

@client.event
async def on_ready():
    logging_blacklist.append(config['logging_blacklist'])
    logging_blacklist.append(client.user.id)
    print('Logged in as '+client.user.name+' (ID:'+client.user.id+') | Connected to '+str(len(client.servers))+' servers | Connected to '+str(len(set(client.get_all_members())))+' users')

def timestamp():
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return timestamp

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
        self.server = Utils.get_server(server_id)
        

    def update(self):
        update_dic = {
            'warns':self.warnings,
            'verified':self.verified,
            'in_server':self.present
        }
        db.update(table='members',values=update_dic,params={'id':self.id,'server_id':self.server_id})
        return 1

    def warn(self):
        if self.warnings+1 >= self.server.max_warnings:
                return 2
        else:
            self.warnings = self.warnings+1
            self.update()
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

    def __init__(self,id=0,added_on=0,welcome_channel=0,goodbye_channel=0,event_channel=0,log_channel=0,log_active=0,log_whitelist=0,entry_text=0,entry_text_pm=0,goodbye_text=0,max_warnings=0,votekick=0):
        self.id = id
        self.added_on = added_on
        self.entry_text = entry_text
        self.entry_text_pm = entry_text_pm
        self.goodbye_text = goodbye_text
        self.log_whitelist = log_whitelist
        self.welcome_channel = welcome_channel
        self.goodbye_channel = goodbye_channel
        self.event_channel = event_channel
        self.log_channel = log_channel
        self.log_active = log_active
        self.max_warnings = int(max_warnings)
        self.disc_server = client.get_server(self.id)
        self.name = self.disc_server.name

    def update(self):
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
        db.update(table='servers',values=update_dic,params={'id':str(self.id)})
        return 1

    def get_member(self,id):
        res = db.select(table='members',fields=[
            'warns','verified',
            'in_server'],params={'server_id':self.id,
            'id':id})
        if res:
            user = User(id,self.id,res.warns,res.verified,res.in_server)
            return user

    def make_member(self,id,verified=0):
        db.insert(table='members',values={
            'id':id,
            'server_id':self.id,
            'verified':verified
            })
        return self.get_member(id)

    def toggle_logging_msg(self):
        print(self.log_active['msg'])
        if self.log_active['msg']==0:
            self.log_active['msg']=1
            if self.update():
                return 1              
        else:
            self.log_active['msg']=0
            if self.update():
                return 2

    def toggle_logging_name(self):
        print(self.log_active)        
        if self.log_active['name']==0:
            self.log_active['name']=1
            if self.update():
                return 1              
        else:
            self.log_active['name']=0
            if self.update():
                return 2                

class Utils():

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
        

    def get_server(id):
        result = db.select(table='servers',fields=[
        'added_on','entry_text','entry_text_pm','goodbye_text',
        'log_whitelist','welcome_channel','goodbye_channel','event_channel',
        'log_channel','log_active','max_warns'],params={'id':id})
        id = str(id)
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
        server = Server(id,
        result.added_on,
        result.welcome_channel,
        result.goodbye_channel,
        result.event_channel,
        result.log_channel,
        json.loads(result.log_active),
        log_whitelist,
        result.entry_text,
        result.entry_text_pm,
        result.goodbye_text,
        int(result.max_warns))
        return server

    def make_server(id=0):
        server = Server(id=id)
        db.insert(table='servers',values={'id':id})
        return server
                        
    def delete_server(id):
        db.delete(table='servers',params={'id':id})
        db.delete(table='members',params={'server_id':id})