import discord, random, os, sys, subprocess
from discord.ext import commands, tasks
from discord.utils import *
from itertools import cycle
import logging

client = commands.Bot(command_prefix=commands.when_mentioned_or('+'), case_insensitive=True)
client.remove_command('help')

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))

logger.addHandler(handler)

@client.command()
@commands.is_owner()
async def reload(ctx, cog):
    """Reload a cog. (Bot owner only)"""
    await ctx.trigger_typing()
    try:
        client.unload_extension(f'cogs.{cog}')
        client.load_extension(f'cogs.{cog}')
        embed=discord.Embed(title="Success!", color=0x008000)
        embed.add_field(name="Reloaded:", value=f"{cog}", inline=False)
        await ctx.send(embed=embed)
    except Exception as e:
        embed=discord.Embed(title="Error", color=0xff2d2d)
        embed.add_field(name=f"{cog} could not be reloaded.", value=f"Detected error: {e}", inline=False)
        await ctx.send(embed=embed)
        print(f'The module {cog} could not be loaded.')
        raise e

@client.command()
@commands.is_owner()
async def load(ctx, cog):
    """Load a cog. (Bot owner only)"""
    await ctx.trigger_typing()
    try:
        client.load_extension(f'cogs.{cog}')
        embed=discord.Embed(title="Success!", color=0x008000)
        embed.add_field(name="Loaded:", value=f"{cog}", inline=False)
        await ctx.send(embed=embed)
    except Exception as e:
        embed=discord.Embed(title="Error", color=0xff2d2d)
        embed.add_field(name=f"{cog} could not be loaded.", value="Is it already loaded?", inline=False)
        await ctx.send(embed=embed)
        print(f'The module {cog} could not be loaded.')
        raise e

@client.command()
@commands.is_owner()
async def unload(ctx, cog):
    """Unload a cog. (Bot owner only)"""
    await ctx.trigger_typing()
    try:
        client.unload_extension(f'cogs.{cog}')
        embed=discord.Embed(title="Success!", color=0x008000)
        embed.add_field(name="Unloaded:", value=f"{cog}", inline=False)
        await ctx.send(embed=embed)
    except Exception as e:
        embed=discord.Embed(title="Error", color=0xff2d2d)
        embed.add_field(name=f"{cog} could not be unloaded.", value="Is it already unloaded?", inline=False)
        await ctx.send(embed=embed)
        print(f'The module {cog} could not be loaded.')
        raise e

@client.event
async def on_ready():
    print("#---------------------------#")
    print("#                           #")
    print("#         Logged in         #")
    print("#    Walter_Clements_Bot    #")
    print("#                           #")
    print("#---------------------------#")

    change_status.start()


#                               #
#       DM Autorresponder       #
#                               #

@client.event
async def on_message(message):
    if message.guild is None:
        responses = ['Hey there.', 'bruh',
                    'walter', 'i will eat you', 
                    'Leave me alone', 'Nothing to see here...', 
                    'Go away', 'Haha yeah', 
                    'oof', 'Should I know you?', 
                    'affirmative', 'where am i', 
                    'hope you\'re having a nice day', 'never dm me again',
                    'how are you', 'NO',
                    'i literally could not care less', 'don\'t remember asking',
                    'i would have to go with yes', 'am confused',
                    'why are you talking to a robot', 'i don\'t care',
                    'sure', 'dms are closed go home',
                    'bup', 'what do you think',
                    'trust no one', 'of course',
                    'don\'t you have something better to do?', '?',
                    'no u', 'no can do',
                    'psssst... i\'m not a real person', 'go clean your room',
                    'wee snaw', '*cries*',
                    'owo', 'I\'m sorry, but you do not have permission to perform this command. Please contact the server administrators if you think this is an error.',
                    'how are you not in school?', 'fantastic',
                    'who put you on the planet', 'get a life',
                    'do you are have stupid', 'despacito',
                    'if you say so', 'don\'t think so',
                    'hope you\'re having a nice day', 'QUIET DOWN I\'M PLAYING FORTNITE',
                    'take care!', 'you can go now',
                    'pizza time', 'quit horsing around!',
                    'huh?', 'shut up',
                    'amazing', 'yo',
                    'aaaaaaa', 'ok',
                    'loser']
        await message.author.send(random.choice(responses))
    else:
        try:
            await client.process_commands(message)
        except:
            pass

@tasks.loop(seconds=30) 
async def change_status():
    for guild in client.guilds:
        totalMembers += guild.member_count
    if random.randint(1, 2) == 1:
        activity = discord.Activity(name=f"{totalMembers} in {len(client.guild)} servers", type=discord.ActivityType.watching)
    else:
        activity = discord.Activity(name=f"for +help", type=discord.ActivityType.watching)
    await client.change_presence(activity=activity)

for cog in os.listdir(".\\cogs"):
    if cog.endswith(".py"):
        try:
            cog = f"cogs.{cog.replace('.py', '')}"
            client.load_extension(cog)
        except Exception as e:
            print(f'{cog} cannot be loaded:')
            raise e


with open("config.json", "r") as f:
    config = json.load(f)
    f.close()

client.run(config["token"])
