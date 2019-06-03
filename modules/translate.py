from pbot_utils import client,config,logger,Utils
from aiohttp import ClientSession
from json import dumps

lang_codes = ['ab', 'aa', 'af', 'ak', 'sq', 'am', 'ar', 'an', 'hy', 'as', 'av', 'ae', 'ay', 'az', 'bm', 'ba', 'eu', 'be', 'bn', 'bh', 'bi', 'bs', 'br', 'bg', 'my', 'ca', 'ch', 'ce', 'ny', 'zh', 'cv', 'kw', 'co', 'cr', 'hr', 'cs', 'da', 'dv', 'nl', 'dz', 'en', 'eo', 'et', 'ee', 'fo', 'fj', 'fi', 'fr', 'ff', 'gl', 'ka', 'de', 'el', 'gn', 'gu', 'ht', 'ha', 'he', 'hz', 'hi', 'ho', 'hu', 'ia', 'id', 'ie', 'ga', 'ig', 'ik', 'io', 'is', 'it', 'iu', 'ja', 'jv', 'kl', 'kn', 'kr', 'ks', 'kk', 'km', 'ki', 'rw', 'ky', 'kv', 'kg', 'ko', 'ku', 'kj', 'la', 'lb', 'lg', 'li', 'ln', 'lo', 'lt', 'lu', 'lv', 'gv', 'mk', 'mg', 'ms', 'ml', 'mt', 'mi', 'mr', 'mh', 'mn', 'na', 'nv', 'nb', 'nd', 'ne', 'ng', 'nn', 'no', 'ii', 'nr', 'oc', 'oj', 'cu', 'om', 'or', 'os', 'pa', 'pi', 'fa', 'pl', 'ps', 'pt', 'qu', 'rm', 'rn', 'ro', 'ru', 'sa', 'sc', 'sd', 'se', 'sm', 'sg', 'sr', 'gd', 'sn', 'si', 'sk', 'sl', 'so', 'st', 'az', 'es', 'su', 'sw', 'ss', 'sv', 'ta', 'te', 'tg', 'th', 'ti', 'bo', 'tk', 'tl', 'tn', 'to', 'tr', 'ts', 'tt', 'tw', 'ty', 'ug', 'uk', 'ur', 'uz', 've', 'vi', 'vo', 'wa', 'cy', 'wo', 'fy', 'xh', 'yi', 'yo', 'za', 'zu']
translate_enabled = {}

session = ClientSession(headers={"Content-Type":"application/json; charset=utf-8"})

class Translate:
    def __init__(self,source=None,target='en'):
        self.source = source
        self.target = target

    async def translate(self,message):
        res = await session.post("https://translation.googleapis.com/language/translate/v2?key={}".format(config['gcloud_api']),data=dumps({'source':self.source,'target':self.target,'format':'text','q':message}))
        if res.status==200:
            res = await res.json()
            return (res["data"]["translations"][0]["translatedText"],res["data"]["translations"][0]["detectedSourceLanguage"] if not self.source else self.source)
        else:
            logger.error(await res.text())


@client.group(pass_context=True,invoke_without_command=True)
async def translate(ctx,source=None,target='en'):
    if ctx.invoked_subcommand:
        return
    if not Utils.check_perms_ctx(ctx,'manage_channels'):
        return await client.say(config['error_permissions'].format('Manage Channels'))
    if ctx.message.channel.id in translate_enabled:
        await client.say("Disabling translation for this channel")
        translate_enabled.pop(ctx.message.channel.id,None)
        return 
    if not source or source in lang_codes and target in lang_codes:
        translate_enabled[ctx.message.channel.id] = Translate(source=source,target=target)
        return await client.say("Translate enabled for {} (From:{} to {})".format(ctx.message.channel.name,"all" if not source else source,target))
    return await client.say("Invalid source or target language")

@translate.command()
async def message(source='auto',target='en',*msg):
    if len(msg)==0:
        return await client.say("No message given")
    else:
        msg = " ".join(msg)
    if source=='auto':
        source = None
    trsl = Translate(source,target)
    msg = await trsl.translate(msg)
    return await client.say("**[{}]** {}".format(msg[1],msg[0]))

@client.listen('on_message')
async def message_event(message):
    if message.author==client.user or message.content.startswith(">>"):
        return
    if message.channel.id in translate_enabled:
        msg = await translate_enabled[message.channel.id].translate(message.content)
        if msg[1]!=translate_enabled[message.channel.id].target:
            return await client.send_message(message.channel,"**__[{}]__ <{}>** {}".format(msg[1].upper(),message.author.name,msg[0]))
        