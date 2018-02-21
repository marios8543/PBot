import json
import discord
import asyncio
import mysql.connector
from datetime import datetime
from discord.ext.commands import Bot
from discord.ext import commands
import lxml.html
from urllib.request import urlopen
import hashlib
from random import randint
import time
import codecs
import os
#from modules import *

warn_whitelist=['196224042988994560','180800780960399361','207559404466208779','386505899713495051']
logging_blacklist=['196224042988994560','351236161684897792','381066546535202816']

#Create database connection
conn = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='pbot')
db = conn.cursor(buffered=True)

#Initial database caching
db.execute("SELECT server_id,welcome_channel,goodbye_channel,event_channel,log_channel,log_msgchanges,log_whitelist,entry_text,goodbye_text,entry_text_pm FROM servers")
data = db.fetchall()
w_channels = {}
g_channels = {}
e_channels = {}
l_channels = {}
log_status = {}
log_wlists = {}
w_txt = {}
g_txt = {}
wpm_txt = {}
for srv in data:
    w_channels[str(srv[0])] = str(srv[1])
    g_channels[str(srv[0])] = str(srv[2])
    e_channels[str(srv[0])] = str(srv[3])
    l_channels[str(srv[0])] = str(srv[4])
    log_status[str(srv[0])] = str(srv[5])
    log_wlists[str(srv[0])] = str(srv[6].decode('utf-8'))
    w_txt[str(srv[0])] = str(srv[7].decode('utf-8'))
    g_txt[str(srv[0])] = str(srv[8].decode('utf-8'))
    wpm_txt[str(srv[0])] = str(srv[9].decode('utf-8'))

#Function for removing non-ascii characters that can't be stored in the database
def remove_non_ascii(text):
    return ''.join([i if ord(i) < 128 else ' ' for i in str(text)])

#Initial setup
client = Bot(description="pbot_public", command_prefix=">>")
@client.event
async def on_ready():
    #print('Logged in as '+client.user.name+' (ID:'+client.user.id+') | Connected to '+str(len(client.servers))+' servers | Connected to '+str(len(set(client.get_all_members())))+' users github.com/marios8543/PBot/')
    await client.change_presence(game=discord.Game(name="DON'T type >>help"))
    modules = os.listdir('modules')
    modules = ' ,'.join(map(str, modules))
    print(modules)
    for server in client.servers:
        channel = client.get_channel(e_channels[server.id])
        message ='''.
        ***>PBot 1.0***

        Made with :heart: by Uwumin (tzatzikiweeb#7687)
        https://github.com/marios8543/PBot

        >Implying we can programming
        https://discord.gg/XACSrhZ

        -----------------------Diagnostics----------------------

        Logged in as %s (ID:%s)

        Serving %s servers and %s users

        MySQL connection: %s

        MySQL version: %s
        ''' %(str(client.user.name),str(client.user.id),str(len(client.servers)),str(len(set(client.get_all_members()))),str(conn.is_connected()),str(conn.get_server_info().decode("utf-8")))
        await client.send_message(channel,message)



#token = open("token.txt",'r').read()
#print(token)
client.run('MzcxMzcwMzIxNDAxNjEwMjQx.DW9Krw.dKiCbAaeuj67LZakRdQWDr6lUVY')
