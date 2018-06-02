"""
from pbot_utils import *

class Item():

	def __init__(self,id,name,creator,links,description,tags):
		self.id = id
		self.name = name
		self.creator = creator
		self.creator_name = str(client.get_user_info(self.creator))
		self.links = json.loads(links)
		self.description = description
		self.tags = tags.split(',')

	async def save(self):
		db.insert(table='storage',values={
			'id':self.id,
			'creator':self.creator,
			'links':json.dumps(self.links),
			'description':self.description,
			'tags':','.join(self.tags)
		})
		return 1

	def make_embed(self,send=1):
		embed = discord.Embed(title=self.name)
		embed.set_author(name=self.creator_name)
		#TODO make storage
"""		

