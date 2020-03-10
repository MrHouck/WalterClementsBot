import discord, datetime, time
from discord.ext import commands

start_time = time.time()

class BotStats(commands.Cog):
    def __init__(self, client):
        self.bot = client

    @commands.command()
    async def uptime(self, ctx):
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
        #UPTIME
        current_time = time.time()
        difference = current_time - start_time
        text = str(datetime.timedelta(seconds=difference))
        #GUILDS
        guildNum = len(self.bot.guilds)
        #get users
        totalMembers = 0
        for guild in self.bot.guilds:
            totalMembers += guild.member_count

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
        for guild in self.bot.guilds:
            print(f'In guild {guild.name} (ID: {guild.id}), has {guild.member_count} members.')

def setup(client):
    client.add_cog(BotStats(client))
    now = datetime.datetime.now()
    print(f"{now} | Loaded botstats module.")
