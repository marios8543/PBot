import aiopg
import asyncio
import json
import aiosqlite3
from misc.queries import queries

with open("config.json","r+") as config:
    config = json.loads(config.read())   

async def main():
	conn = await aiopg.connect(database=config['db_database'],user=config['db_user'],
	password=config['db_password'],host=config['db_address'],port=5433)
	db = await conn.cursor()
	print("Checking database...")
	for q in queries:
		await db.execute(q)
	print("Done")
	sconn = await aiosqlite3.connect(database="pbot.db")
	sdb = await sconn.cursor()
	print("Migrating servers")
	await sdb.execute("SELECT * FROM servers WHERE 1")
	res = await sdb.fetchall()
	for i in res:
		phld = ""
		for ii in i:
			phld+="%s,"
		await db.execute("INSERT INTO servers values({})".format(phld[:-1]),i)
	print("Migrating members")
	await sdb.execute("SELECT * FROM members WHERE 1")
	res = await sdb.fetchall()
	for i in res:
		phld = ""
		for ii in i:
			phld+="%s,"
		await db.execute("INSERT INTO members values({})".format(phld[:-1]),i)
	print("Migrating setting_sessions")
	await sdb.execute("SELECT * FROM setting_sessions WHERE 1")
	res = await sdb.fetchall()
	for i in res:
		phld = ""
		for ii in i:
			phld+="%s,"
		await db.execute("INSERT INTO users values({})".format(phld[:-1]),i)
	print("All done. Exiting...")
    
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
