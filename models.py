import json
import unicodedata
from datetime import datetime
from pbot_utils import db

def ascii_convert(s):
    return unicodedata.normalize('NFKD', s).encode('ascii','ignore')

def get_timestamp():
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return timestamp

class User():
    id = ""
    id = ""
    name = ""
    join_date = ""
    info = ""
    warnings = 0
    verified = 0
    present = 0

    def update(self):
        update_dic = {}
        base = self.base
        for prop,value in vars(self).iteritems():
            if getattr(base,prop)!=value:
                update_dic[prop] = value
        if db.update(table='users',values=update_dic,params={'user_id':self.id}):
            return 1

    def warn(self):
        if self.warnings >= get_server(self.id).max_warnings:
                return 2
        else:
            self.warnings = self.warnings+1
            self.update()
            return 1

class Server():
    id = ""
    server_name = ""
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

    def update(self):
        update_dic = {}
        for prop,value in vars(self).items():
            update_dic[value]=prop
        print(update_dic)
        db.update(table='servers',values=update_dic,params={'id':str(self.id)})
        return 1

    def get_member(self,id):
        db.execute("""SELECT discord_id,
                   discord_name,
                   join_date,
                   warns,
                   verified,
                   in_server
                   FROM members
                   WHERE id=%s AND discord_id=%s""",(self.id,id,))
        res = db.fetchone()
        if res:
            user = User()
            user.id = res[0]
            user.id = self.id
            user.name = res[1]
            user.join_date = res[2]
            user.warnings = res[3]
            user.verified = res[4]
            user.present = res[5]
            return user

    def make_member(self,name,id,joindate):
        name = ascii_convert(name)
        timestamp = get_timestamp()
        if db.execute("INSERT into members (discord_name,discord_id,id,join_date) values(%s,%s,%s,%s)",(name,id,self.id,joindate,)):
            conn.commit()
            return self.get_member(id)
