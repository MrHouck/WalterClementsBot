import discord, datetime, time, json
from discord.ext import commands, tasks
import random
import os
import requests
import urllib3
start_time = time.time()
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

class BotStats(commands.Cog):
    def __init__(self, client):
        self.bot = client

    @commands.command()
    async def uptime(self, ctx):
        """
        Get the uptime of the bot.
        """
        current_time = time.time()
        difference = current_time - start_time
        text = str(datetime.timedelta(seconds=difference))
        embed = discord.Embed(color=ctx.author.color)
        embed.add_field(name="Uptime", value=text)
        try:
            await ctx.send(embed=embed)
        except discord.HTTPException:
            await ctx.send("Current uptime: " + text)

    @commands.command()
    async def botstats(self, ctx):
        """
        Get statistics of the bot.
        """
        #UPTIME
        current_time = time.time()
        difference = current_time - start_time
        text = str(datetime.timedelta(seconds=difference))
        #GUILDS
        guildNum = len(self.bot.guilds)
        #get users
        totalMembers = 0
        for guild in self.bot.guilds:
            for member in guild.members:
                if not member.bot:
                    totalMembers+=1
        ping = self.bot.latency
        if ping < 100:
            color = discord.Color.green()
        elif ping > 100 and ping < 200:
            color = discord.Color.from_rgb(0, 34, 255)
        else:
            color = discord.Color.red()
        embed = discord.Embed(title="Walter Clements Bot Statistics", color=color)
        embed.add_field(name="Uptime", value='{}'.format(text))
        embed.add_field(name="Guild Count", value='{}'.format(guildNum), inline=False)
        embed.add_field(name="Total Members", value='{}'.format(totalMembers), inline=False)
        embed.add_field(name="Client Latency", value='{}ms'.format(round(ping*1000)), inline=False)
        await ctx.send(embed=embed)
        
def setup(client):
    client.add_cog(BotStats(client))
    now = datetime.datetime.now()
    print(f"{now} | Loaded botstats module.")