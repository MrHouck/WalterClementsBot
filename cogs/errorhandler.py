import traceback
import sys
from discord.ext import commands
import discord

class CommandErrorHandler(commands.Cog):
    def __init__(self, client):
        self.bot = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        #prevents hard coded error events from being handled
        if hasattr(ctx.command, 'on_error'):
            return

        ignored = (commands.UserInputError)

        error = getattr(error, 'original', error)

        if isinstance(error, ignored):
            return
        elif isinstance(error, commands.NoPrivateMessage):
            try:
                return await ctx.author.send(f'{ctx.command} cannot be used in direct messages.')
            except:
                pass
        elif isinstance(error, commands.CheckFailure):
            embed = discord.Embed(title="Error", color=0xff2d2d)
            embed.add_field(name="Missing permissions", value="You don't have the permissions to do this!", inline=False)
            embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        elif isinstance(error, commands.CommandNotFound):
            embed = discord.Embed(title="Error", color=0xff2d2d)
            embed.add_field(name="Invalid Command", value="To get a list of commands, use +help", inline=False)
            embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        elif isinstance(error, commands.DisabledCommand):
            embed = discord.Embed(title="Error", color=0xff2d2d)
            embed.add_field(name="Disabled Command", value="This command has been disabled by an administrator.", inline=False)
            embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        elif isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(title="Error", color=0xff2d2d)
            embed.add_field(name="Command is on cooldown", value=f"You must wait {round(error.retry_after,2)} seconds.", inline=False)
            embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        elif isinstance(error, commands.BadArgument):
            if ctx.command.qualified_name == 'tag list':
                return await ctx.send('I could not find that member. Please try again.')
        elif isinstance(error, commands.NotOwner):
            embed = discord.Embed(title="Error", color=0xff2d2d)
            embed.add_field(name="Not Owner", value="You do not own this bot!", inline=False)
            embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        else:
            await ctx.send(error)

        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

def setup(client):
    client.add_cog(CommandErrorHandler(client))
    print('Loaded errorhandler module.')
