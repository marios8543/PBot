print('>PBot1.0 - Made with <3 by Uwumin/tzatzikiweeb - github.com/marios8543/PBot')
from pbot_utils import Utils,config,client
import os
for module in os.listdir(os.path.join(os.path.dirname(__file__),'modules')):
    if module == '__init__.py' or module[-3:] != '.py':
        continue
    print('Imported module {}'.format(module[:-3]))
    __import__('modules.'+module[:-3],fromlist='*')
del module
print('Imports complete. Logging in...')
@client.event
async def on_ready():
    print('Logged in as '+client.user.name+' (ID:'+client.user.id+') | Connected to '+str(len(client.servers))+' servers | Connected to '+str(len(set(client.get_all_members())))+' users')


if __name__=='__main__' and config['debug']=="false":
    client.run(config['token'])
