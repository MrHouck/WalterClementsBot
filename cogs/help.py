import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, client):
        self.bot = client

    @commands.command(pass_context=True)
    @commands.guild_only()
    async def help(self, ctx, command=None):
        if command == None:
            await ctx.trigger_typing()
            embed=discord.Embed(title="Help", color=0x4966cb)
            embed.add_field(name="🥳 **Fun:**", value="``8ball, achievement, fbi, norris, penis, randomname, retard, sentence, uwu, walter``", inline=False)
            embed.add_field(name="🛠️ **Moderation:**", value="``autorole[enable, disable, setrole], ban, clear, createrole, deleterole, logs[enable, disable, setchannel], mute, unban, unmute, role, softban``", inline=False)
            embed.add_field(name="📈 **Economy:**", value="``balance, buy, daily, fish, register, shop, stats, stocks[buy, sell, view]``")
            embed.add_field(name="💎 **Miscellaneous:**", value="``changelog, color, help, invite, serverinfo, usage, userinfo, suggestion``", inline=False)
            embed.set_footer(text="WalterClementsBot - by MrHouck#2775 | v1.7.4")
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Help(client))
