from pbot_utils import *


#Warn command
@client.command(pass_context=True)
async def warn(ctx,user,reason):
    server = ctx.message.server
    srv = Utils.get_server(server.id)
    member2 = ctx.message.author
    if Utils.check_perms_ctx(ctx,'ban_members'):
        if not ctx.message.raw_mentions:
            user_id = user
        else:
            user_id = ''.join(ctx.message.raw_mentions)
        warnman = srv.get_member(user_id)
        if str(user_id) not in warn_whitelist:
            if warnman.warn()==1:
                await client.say(':exclamation: <@!'+str(user_id)+'> has been warned. His warning count is now '+str(warnman.warnings+1)+' ('+str(int(srv.max_warnings)-int(warnman.warnings) -1)+' warns left)')
                embed=discord.Embed(title=":exclamation: User Warned", color=0xed00f9)
                embed.add_field(name="User warned", value=warnman.name, inline=False)
                embed.add_field(name="Admin in charge", value=ctx.message.author.name, inline=False)
                embed.add_field(name="Reason", value=reason, inline=False)
                embed.add_field(name="Warning count", value=str(warns+1)+' ('+str(int(max_warns)-int(warns) -1)+' warns left)', inline=False)
                embed.set_footer(text=str(timestamp()))
                await client.send_message(client.get_channel(srv.log_channel),embed=embed)
            elif warnman.warn()==2:
                member2server = server.get_member(user_id)
                msg = await client.say(':exclamation: User has {} warnings and will be banned! Click on :white_check_mark: to confirm...'.format(warnman.warnings))
                await client.add_reaction(msg,'👍')
                await asyncio.sleep(1)
                res = await client.wait_for_reaction(message=msg)
                if res.reaction.emoji == '👍':
                    await client.ban(member2server)
                    await client.send_message(client.get_user_info(user_id),'You have been banned for breaking the rules. You totally received '+str(warns)+' warnings before being issued a ban.')
            else:
                await client.say(config['default_error'])        
        else:
            await client.say(':negative_squared_cross_mark: Haha nice try cuck. You cant warn me :^)')
    else:
        await client.say(config['error_permissions'].format('Ban Members'))


@client.command(pass_context=True)
async def clearwarnings(ctx,arg):
    server = ctx.message.server
    if Utils.check_perms_ctx(ctx,'ban_members'):
        user_id = ''.join(ctx.message.raw_mentions)
        usr = Utils.get_server(ctx.message.server.id).get_member(user_id)
        usr.warnings = 0
        if usr.update():
            await client.say(':white_check_mark: <@!'+user_id+'> is now clear!')
        else:
            await client.say(config['default_error'])    
    else:
        await client.say(config['error_permissions'].format('Ban Member'))


@client.command(pass_context=True)
async def softban(ctx,arg,arg2):
    if Utils.check_perms_ctx(ctx,'kick_members'):
        if int(arg2) <= int(config['max_softban']):
            unverified = discord.Utils.get(server.roles, name="Unverified")
            if not ctx.message.raw_mentions:
                user_id = arg
            else:
                user_id = ''.join(ctx.message.raw_mentions)
            time = int(arg2)*60
            await client.add_roles(server.get_member(user_id), unverified)
            await client.say(':white_check_mark: <@!'+str(user_id)+'> has been denied access for '+str(arg2)+' minutes...')
            await asyncio.sleep(time)
            await client.remove_roles(server.get_member(user_id), unverified)
            await client.say('<@!'+str(user_id)+'> is here again!')
        else:
            await client.say(':negative_squared_cross_mark: Maximum softban time is {} minutes'.format(config['max_softban']))
    else:
        await client.say(config['error_permissions'].format('Kick Members'))