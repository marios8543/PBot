print('>PBot1.0 - Made with <3 by Uwumin/tzatzikiweeb - github.com/marios8543/PBot')
from pbot_utils import Utils,config,client
import os
import uvloop
import asyncio
for module in os.listdir(os.path.join(os.path.dirname(__file__),'modules')):
    if module == '__init__.py' or module[-3:] != '.py':
        continue
    print('Imported module {}'.format(module[:-3]))
    __import__('modules.'+module[:-3],fromlist='*')
del module
print('Imports complete. Logging in...')

if __name__=='__main__' and config['debug']=="false":
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    client.run(config['token'])
