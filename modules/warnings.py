from pbot_utils import *


#Warn command
@client.command(pass_context=True)
async def warn(ctx,user,*reason):
    if not reason:
        return await client.say(":negative_squared_cross_mark: No reason provided")
    reason = " ".join(reason)
    server = ctx.message.server
    srv = await Utils.get_server(server.id)
    if Utils.check_perms_ctx(ctx,'ban_members'):
        if not ctx.message.raw_mentions:
            user_id = user
        else:
            user_id = ''.join(ctx.message.raw_mentions)
        warnman = await srv.get_member(user_id)
        warns = warnman.warnings
        max_warns = srv.max_warnings
        if str(user_id) not in warn_whitelist:
            if await warnman.warn()==1:
                await client.say(':exclamation: <@!'+str(user_id)+'> has been warned. His warning count is now '+str(warnman.warnings+1)+' ('+str(int(srv.max_warnings)-int(warnman.warnings) -1)+' warns left)')
                embed=discord.Embed(title=":exclamation: User Warned", color=0xed00f9)
                embed.add_field(name="User warned", value=warnman.name, inline=False)
                embed.add_field(name="Admin in charge", value=ctx.message.author.name, inline=False)
                embed.add_field(name="Reason", value=reason, inline=False)
                embed.add_field(name="Warning count", value=str(warns+1)+' ('+str(int(max_warns)-int(warns) -1)+' warns left)', inline=False)
                embed.set_footer(text=str(timestamp()))
                await client.send_message(client.get_channel(srv.log_channel),embed=embed)
            elif await warnman.warn()==2:
                member2server = server.get_member(user_id)
                msg = await client.say(':exclamation: User has {} warnings and will be banned! Click on :white_check_mark: to confirm...'.format(warnman.warnings))
                await client.add_reaction(msg,'\U0001f44d')
                await asyncio.sleep(1)
                while True:
                    res = await client.wait_for_reaction(message=msg)
                    if res.reaction.emoji == '\U0001f44d' and res.user==ctx.message.author:
                        await client.ban(member2server)
                        return await client.send_message(member2server,'You have been banned for breaking the rules. You totally received '+str(warns)+' warnings before being issued a ban.')
                    if not res:
                        return
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
        usr = await Utils.get_server(ctx.message.server.id)
        usr = await usr.get_member(user_id)
        usr.warnings = 0
        if await usr.update():
            await client.say(':white_check_mark: <@!'+user_id+'> is now clear!')
        else:
            await client.say(config['default_error'])    
    else:
        await client.say(config['error_permissions'].format('Ban Member'))

muted_users = []

@client.command(pass_context=True)
async def mute(ctx,arg,time=0):
    server = ctx.message.server
    if Utils.check_perms_ctx(ctx,'manage_roles'):
        unverified = discord.utils.get(ctx.message.server.roles, name="Unverified")
        try:
            time = int(time)
        except Exception:
            return await client.say(":negative_squared_cross_mark: Invalid time provided")
        if not ctx.message.raw_mentions:
            user_id = arg
        else:
            user_id = ''.join(ctx.message.raw_mentions)
        member = server.get_member(user_id)
        if not member:
            return await client.say(":negative_squared_cross_mark: Invalid member provided")
        if time==0:
            await client.add_roles(member,unverified)
            muted_users.append(user_id)
            return await client.say(":white_check_mark: {} has been muted for an indefinite amount of time".format(str(member)))
        if time <= int(config['max_softban']):
            await client.add_roles(member,unverified)
            muted_users.append(user_id)
            await client.say(":white_check_mark: {} has been muted for {} minutes".format(str(member),time))
            for i in range(time*60):
                if user_id in muted_users:
                    await asyncio.sleep(1)
                else:
                    return
            muted_users.remove(user_id)
            await client.remove_roles(member,unverified)
            await client.say('<@!'+str(user_id)+'> is here again!')
        else:
            await client.say(':negative_squared_cross_mark: Maximum softban time is {} minutes'.format(config['max_softban']))
    else:
        await client.say(config['error_permissions'].format('Kick Members'))

@client.command(pass_context=True)
async def unmute(ctx,arg):
    if Utils.check_perms_ctx(ctx,'manage_roles'):
        unverified = discord.utils.get(ctx.message.server.roles, name="Unverified")
        if not ctx.message.raw_mentions:
            user_id = arg
        else:
            user_id = ''.join(ctx.message.raw_mentions)
        member = ctx.message.server.get_member(user_id)
        if not member:
            return await client.say(":negative_squared_cross_mark: Invalid member provided")
        if user_id in muted_users or unverified in member.roles:
            try:
                muted_users.remove(user_id)
            except Exception:
                pass
            await client.remove_roles(member,unverified)
            return await client.say(":white_check_mark: {} has been unmuted".format(str(member)))

