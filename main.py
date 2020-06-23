import discord, random, os, sys, subprocess
from discord.ext import commands, tasks
import datetime
import time, requests
from discord.utils import *
from itertools import cycle
start_time = time.time()

client = commands.Bot(command_prefix='+', case_insensitive=True)
client.remove_command('help')

@client.group(invoke_without_subcommand=False, hidden=True)
@commands.is_owner()
async def cmd(ctx):
    pass

@cmd.command(usage="<command>")
async def enable(ctx, command: str):
    c = client.get_command(command)
    if c is None:
        return await ctx.send("Command not found.")
    elif c.enabled is True:
        return await ctx.send("Command is already enabled.")
    else:
        c.enabled = True
        return await ctx.send(f"{command} is now enabled")

@cmd.command(usage="<command>")
async def disable(ctx, command: str):
    c = client.get_command(command)
    if c is None:
        return await ctx.send("Command not found.")
    elif c.enabled is False:
        return await ctx.send("Command is already disabled.")
    else:
        c.enabled = False
        return await ctx.send(f"{command} is now disabled")



@client.command(usage="<cog>")
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

@client.command(usage="<cog>")
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

@client.command(usage="<cog>")
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
    now = datetime.datetime.now()
    print(f'{now} | Logged in.')
    change_status.start()

@client.event
async def on_guild_join(guild):
    channel = client.get_channel(713047567411445842)
    await channel.send(f"Joined {guild.name} (ID: {guild.id})\nHas {guild.member_count} members.")

@client.event
async def on_guild_leave(guild):
    channel = client.get_channel(713047567411445842)
    await channel.send(f"Removed from {guild.name} (ID: {guild.id})")



#                               #
#       DM Autorresponder       #
#                               #

@client.event
async def on_message(message):
    if message.guild is None:
        responses = ['Hey there.', 'bruh','walter', 'i will eat you', 
                    'Leave me alone', 'Nothing to see here...', 'Go away', 'Haha yeah', 
                    'oof', 'Should I know you?', 'affirmative', 'where am i', 
                    'hope you\'re having a nice day', 'never dm me again', 'how are you', 'NO',
                    'i literally could not care less', 'don\'t remember asking', 'i would have to go with yes', 'am confused',
                    'why are you talking to a robot', 'i don\'t care', 'sure', 'dms are closed go home',
                    'bup', 'what do you think', 'trust no one', 'of course',
                    'don\'t you have something better to do?', '?', 'no u', 'no can do',
                    'psssst... i\'m not a real person', 'go clean your room', 'wee snaw', '*cries*',
                    'owo', 'I\'m sorry, but you do not have permission to perform this command. Please contact the server administrators if you think this is an error.',
                    'how are you not in school?', 'fantastic', 'who put you on the planet', 'get a life',
                    'do you are have stupid', 'despacito', 'if you say so', 'don\'t think so',
                    'hope you\'re having a nice day', 'QUIET DOWN I\'M PLAYING FORTNITE', 'take care!', 'you can go now',
                    'pizza time', 'quit horsing around!', 'huh?', 'shut up',
                    'amazing', 'yo', 'aaaaaaa', 'ok',
                    'loser', 'that would be a solid nope', 'ngl, kinda hot', 'why are you like this',
                    'stfu', 'please stop talking', 'begone', 'i hate you',
                    'just go', 'hey check out the new website', 'what year is it', 'hey add me to your server',
                    'what do you think of cats', 'uhhhhhhhhh', 'i\'m calling the FBI', 'yes officer, this man right here',
                    'FBI OPEN UP', 'eW91IGhhdmUgbm8gbGlmZQ==', '...', 'lol',
                    'yeah', 'oh', 'RIP +penis', 'that is mildly wack', 
                    'wack', 'uwu', 'thank you for hosting the bot ziad', 'same',
                    'thanks', 'can\'t relate', 'dude are you serious just LEAVE', 'do you know how long it took to write these responses',
                    'yea yea yea i\'m trying to fix stuff', 'leave me alone', 'what did the cat say to the dog\nmeow' ]
        try:
            await message.author.send(random.choice(responses))
        except:
            pass
    else:
        try:
            await client.process_commands(message)
        except:
            pass

@tasks.loop(seconds=30) 
async def change_status():
    if random.randint(1, 2) == 1:
        totalMembers = 0
        for guild in client.guilds:
            totalMembers += guild.member_count
        activity = discord.Activity(name=f"{totalMembers} users in {len(client.guilds)} servers", type=discord.ActivityType.watching)
    else:
        activity = discord.Activity(name=f"for +help", type=discord.ActivityType.watching)
    await client.change_presence(activity=activity)




for cog in os.listdir("./cogs"):
    if cog.endswith(".py"):
        try:
            cog = f"cogs.{cog.replace('.py', '')}"
            client.load_extension(cog)
        except Exception as e:
            print(f'{cog} cannot be loaded:')
            raise e

with open("./cogs/resources/config.json", "r") as f:
    config = json.load(f)
    f.close()

client.run(config["token"])