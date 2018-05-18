from pbot_utils import *
emoji_unicode = {':regional_indicator_a:':'\U0001f1e6',':regional_indicator_b:':'\U0001f1e7',':regional_indicator_c:':'\U0001f1e8',':regional_indicator_d:':'\U0001f1e9',':regional_indicator_e:':'\U0001f1ea'}
choice_emojis = [':regional_indicator_a:',':regional_indicator_b:',':regional_indicator_c:',':regional_indicator_d:',':regional_indicator_e:']
votes_running = {}

def vote_running(ctx):
    for vote in votes_running:
        if votes_running[vote].channel is ctx.message.channel:
            return votes_running[vote]
    
class Vote():
    id = ""
    user = ""
    channel = ""
    question = ""
    options = []
    duration = 0
    embed = 0
    embed_obj = 0
    target = 0
    running = 1

    def __init__(self,ctx,question=0,options=0,duration=0,votetype=0,target=0):
        if votetype==0:
            self.options.clear()
            self.id = ctx.message.id
            self.user = ctx.message.author
            self.channel = ctx.message.channel
            self.question = question
            for idx,option in enumerate(options):
                self.options.append({
                'emoji':choice_emojis[idx],
                'option':option,
                'votes':[]
                })
            self.duration = duration
        if votetype==1:
            self.options.clear()
            self.id = ctx.message.id
            self.user = ctx.message.author
            self.channel = ctx.message.channel
            self.target = target
            self.question = 'Should {}#{} be kicked ?'.format(target.name,target.discriminator)
            self.options.append({
                'emoji':choice_emojis[0],
                'option':'Yes',
                'votes':[]
            })
            self.options.append({
                'emoji':choice_emojis[1],
                'option':'No',
                'votes':[]
            })
            self.duration = 300

    async def make_embed(self,send=1):
        embed = discord.Embed(title=self.question)
        embed.set_author(name="Vote by {}".format(self.user.name+'#'+self.user.discriminator))
        if self.duration>60:
            duration = str(self.duration//60)+' minutes remaining'
        else:
            duration = str(self.duration)+' seconds remaining'
        embed.set_footer(text=duration)
        embed.fields.clear()   
        for option in self.options:
            embed.add_field(name=option['emoji']+' '+option['option'],value='0 votes')
        self.embed_obj = embed
        if send==1:
            self.embed = await client.send_message(self.channel,embed=embed)
            votes_running[self.embed.id] = self
            return {'embed':embed,'msg':self.embed}
        else:
            return embed

    async def add_vote(self,user,option):
        if user.id not in self.options[option]['votes']:
            self.options[option]['votes'].append(user.id)
            embed = self.embed_obj
            if len(self.options[option]['votes'])==1:
                update_str = str(len(self.options[option]['votes']))+' vote'
            else:
                update_str = str(len(self.options[option]['votes']))+' votes'	
            embed.set_field_at(option,name=embed.fields[option].name,value=update_str)
            await client.edit_message(self.embed,embed=embed)
            return 1

    async def remove_vote(self,user,option):
        if user.id in self.options[option]['votes']:
            self.options[option]['votes'].remove(user.id)
            embed = self.embed_obj
            if len(self.options[option]['votes'])==1:
                update_str = str(len(self.options[option]['votes']))+' vote'
            else:
                update_str = str(len(self.options[option]['votes']))+' votes'	
            embed.set_field_at(option,name=embed.fields[option].name,value=update_str)
            await client.edit_message(self.embed,embed=embed)			
            return 1

    def get_winner(self,make_embed=0):
        votes = []
        for idx,vote in enumerate(self.options):
            votes.append(len(vote['votes']))
        if len(set(votes)) <= 1:
            winner = 6
        else:
            winner = votes.index(max(votes))
        if make_embed==0:
            votes_running.pop(self.embed.id,None)
            return winner
        if winner==6:
            embed=discord.Embed(title='The vote is a draw!!!')
        else:    
            embed=discord.Embed(title='The answer is '+self.options[winner]['option'])    
        embed.set_author(name=self.question)
        for option in self.options:
            embed.add_field(name=option['option'],value=str(len(option['votes']))+' votes')
        embed.set_footer(text='Vote called by '+self.user.name+'#'+self.user.discriminator)
        votes_running.pop(self.embed.id,None)
        return embed

    def kill(self):
        self.running=0
        return 1   



@client.group(pass_context=True)
async def vote(ctx):    
    if ctx.invoked_subcommand is None:
        if vote_running(ctx):
            return await client.say(':negative_squared_cross_mark: You can only have one vote running per channel')            
        question = ""
        options = []
        duration = 0
        #Argument parsing
        await client.say(":pencil: Enter the vote question...")
        msg = await client.wait_for_message(timeout=60,author=ctx.message.author,channel=ctx.message.channel)
        if msg:
            question = msg.content
        else:
            return await client.say(':zzz: Vote call timed out...')
        await client.say(':pencil: Ok now enter your choices seperated with `//`...')
        msg = await client.wait_for_message(timeout=60,author=ctx.message.author,channel=ctx.message.channel)
        if msg:
            options = msg.content.split('//')
            if len(options)>5:
                return client.say(":negative_squared_cross_mark: You can't have more than 5 options")   
        else:
            return await client.say(':zzz: Vote call timed out...')
        await client.say(':pencil: Ok finally how long do you want your vote to last. Type just the number in seconds. Max is {} minutes'.format(config['max_softban']))
        msg = await client.wait_for_message(timeout=60,author=ctx.message.author,channel=ctx.message.channel)
        if msg:
            duration = int(''.join(filter(str.isdigit, msg.content)))
            if duration>int(config['max_softban'])*60:
                return await client.say(':negative_squared_cross_mark: Max vote time is {} minutes'.format(config['max_softban']))
        else:
            return await client.say(':zzz: Vote call timed out...')
        #Vote creation 
        vote = Vote(ctx,question,options,duration)
        msg = await vote.make_embed()
        msg = msg['msg']
        for option in vote.options:
            await client.add_reaction(msg,emoji_unicode[option['emoji']])
        #Timer implementation (rewrite pending)
        elapsed = 0
        while vote.duration-1>=elapsed:
            if vote.running!=1:
                await client.delete_message(msg)        
                winner = vote.get_winner(make_embed=1)
                await client.say(embed=winner)    
                return await client.say(':anger: Vote has been canceled')
            await asyncio.sleep(1)
            elapsed = elapsed+1
            remaining = vote.duration-elapsed
            if remaining>60:
                remaining = str(remaining//60)+' minutes remaining'
            else:
                remaining = str(remaining)+' seconds remaining'
            if vote.embed_obj.footer.text!=remaining:
                vote.embed_obj.set_footer(text=remaining)
                await client.edit_message(msg,embed=vote.embed_obj) 
        await client.delete_message(msg)        
        winner = vote.get_winner(make_embed=1)
        await client.say(embed=winner)
        return 1


@vote.command(pass_context=True)
async def kick(ctx):
    if vote_running(ctx):
        return await client.say(':negative_squared_cross_mark: You can only have one vote running per channel')    
    if await Utils.get_server(ctx.message.server.id).log_active['votekick']=='1':
        user = ctx.message.server.get_member(''.join(ctx.message.raw_mentions))
        vote = Vote(ctx,votetype=1,target=user)
        msg = await vote.make_embed()
        embed=msg['embed']
        msg=msg['msg']
        for option in vote.options:
            await client.add_reaction(msg,emoji_unicode[option['emoji']])        
        elapsed = 0
        while vote.duration-1>=elapsed:
            if vote.running!=1:
                return await client.say(':anger: Vote has been canceled')
            await asyncio.sleep(1)
            elapsed = elapsed+1
            remaining = vote.duration-elapsed
            if remaining>60:
                remaining = str(remaining//60)+' minutes remaining'
            else:
                remaining = str(remaining)+' seconds remaining'
            if embed.footer.text!=remaining:
                embed.set_footer(text=remaining)
                await client.edit_message(msg,embed=embed)
            vote.embed_obj = embed    
        await client.delete_message(msg)
        winner = vote.get_winner(make_embed=0)        
        embed = vote.get_winner(make_embed=1)
        if winner==0:
            await client.say(embed=embed)
            await client.send_message(vote.target,':exclamation: You have been kicked because you have been voted off')
            await client.send_message(vote.target,embed=embed)
            await client.kick(vote.target,reason='Votekicked by {}#{}'.format(vote.user.name,vote.user.discriminator))
        else:
            await client.say(embed=embed)
    else:
        await client.say(':negative_squared_cross_mark: Vote-kicking is disabled in this server...')    
    return 1      


@vote.command(pass_context=True)
async def kill(ctx):
    if not vote_running(ctx):
        return await client.say(':negative_squared_cross_mark: No vote running')
    vote = vote_running(ctx)
    user = ctx.message.author
    if vote.user==user.id or Utils.check_perms_ctx(ctx,'manage_messages'):
        vote.kill()
    else:
        await client.say(':negative_squared_cross_mark: Only the vote creator or people with the `Manage Messages` permission can use this.')    



@client.event
async def on_reaction_add(reaction, user):
    if user.id==client.user.id:
        return	
    if reaction.message.id in votes_running.keys():
        vote = votes_running[reaction.message.id]
        for option in vote.options:
            if user.id in option['votes']:
                return
        for idx,options in enumerate(vote.options):
            if emoji_unicode[options['emoji']] == reaction.emoji:
                await vote.add_vote(user,idx)


@client.event
async def on_reaction_remove(reaction,user):
    if user.id==client.user.id:
        return
    if reaction.message.id in votes_running.keys():
        vote = votes_running[reaction.message.id]
        for idx,options in enumerate(vote.options):
            if emoji_unicode[options['emoji']] == reaction.emoji:
                await vote.remove_vote(user,idx)
