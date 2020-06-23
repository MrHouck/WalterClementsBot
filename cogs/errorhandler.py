import traceback
import sys
import os
import discord
import datetime
from discord.ext import commands
import sqlite3

class CommandErrorHandler(commands.Cog):
    def __init__(self, client):
        self.bot = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        
        #prevents hard coded error events from being handled
        if hasattr(ctx.command, 'on_error'):
            return

        ignored = (commands.BadArgument, commands.ExtensionNotLoaded, commands.ExtensionAlreadyLoaded, commands.ExtensionNotFound, commands.CommandNotFound )
        error = getattr(error, 'original', error)

        if isinstance(error, ignored):
            return
        elif isinstance(error, commands.NoPrivateMessage):
            try:
                return await ctx.author.send(f'{ctx.command} cannot be used in direct messages.')
            except:
                pass
        elif isinstance(error, commands.BotMissingPermissions):
            return await ctx.send("I'm missing permissions to do this!")
        elif isinstance(error, discord.errors.Forbidden):
            return await ctx.send("Uh oh, something went wrong. This is probably due to missing permissions or I'm trying to send a message that is too long.")
        elif isinstance(error, commands.CheckFailure):
            embed = discord.Embed(title="Error", color=0xff2d2d)
            embed.add_field(name="Missing permissions", value="You don't have the permissions to do this!", inline=False)
            embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        elif isinstance(error, commands.DisabledCommand):
            embed = discord.Embed(title="Error", color=0xff2d2d)
            embed.add_field(name="Disabled Command", value="This command is temporarily disabled. If you have a question, [join the official server](https://discord.gg/GdWwJpS)", inline=False)
            embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        elif isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(title="Error", color=0xff2d2d)
            embed.add_field(name="Command is on cooldown", value=f"You must wait {round(error.retry_after,2)} seconds.", inline=False)
            embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        elif isinstance(error, commands.BadArgument):
            return await ctx.send('I could not find that member. Please try again.')
        elif isinstance(error, commands.MissingRequiredArgument):
            usage = "" if not ctx.command.usage else ctx.command.usage
            await ctx.send(f"You are missing 1 or more required arguments. Usage for this command is ``+{ctx.command} {usage}``")
        elif isinstance(error, commands.TooManyArguments):
            await ctx.send("You supplied too many arguments for this command!")
        elif isinstance(error, commands.NotOwner):
            embed = discord.Embed(title="Error", color=0xff2d2d)
            embed.add_field(name="FORBIDDEN", value="no.", inline=False)
            embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        elif isinstance(error, commands.NSFWChannelRequired):
            embed = discord.Embed(title='Error', color=0xff2d2d)
            embed.add_field(name="NSFW Channel Required", value="You need to use this command in an NSFW channel.", inline=False)
            embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        else:
            try:
                await ctx.send("An error has occured.")
                await self.bot.get_channel(723232791751295106).send(f"```=ERROR= \nCommand: {ctx.command}\nError: {type(error)}: {error}```")
            except discord.errors.HTTPException:
                print(error)
                await self.bot.get_channel(723232791751295106).send(f"Error was too large to send in discord. Found in command: {ctx.command}. Error type: {type(error)}")
        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

def setup(client):
    client.add_cog(CommandErrorHandler(client))
    now = datetime.datetime.now()
    print(f'{now} | Loaded errorhandler module.')