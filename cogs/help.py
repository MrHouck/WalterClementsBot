import discord
from discord.ext import commands
from datetime import datetime

class Help(commands.Cog):
    def __init__(self, client):
        self.bot = client

    @commands.command(pass_context=True)
    @commands.guild_only()
    async def help(self, ctx):
        await ctx.trigger_typing()
        if ctx.guild.id != 669042023856340993:
            embed=discord.Embed(title="Help", color=0x4966cb)
            embed.add_field(name="🥳 **Fun:**", value="``8ball, achievement, bird, cat, catfact, chatbot, dog, dogfact, fbi, hug, koalafact, norris, panda, pandafact, penis, randomname, retard, sentence, space, uwu, walter``", inline=False)
            embed.add_field(name="🛠️ **Moderation:**", value="``autorole[enable, disable, setrole], ban, clear, createrole, deleterole, lockdown[on, off], logs[enable(setting), disable(setting), setchannel, settings], mute, unban, unmute, role, softban``", inline=False)
            embed.add_field(name="📈 **Economy/Levels:**", value="``balance, buy, daily, fish, register, shop, stats``")
            embed.add_field(name="💎 **Miscellaneous:**", value="``botstats, changelog, complementary, google, hex, help, invite, serverinfo, source, suggestion, uptime, userinfo, urban, wikipedia``", inline=False)
            embed.set_footer(text="WalterClementsBot - by MrHouck#2775 | v1.8.4")
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title="Help", color=0x4966cb)
            embed.add_field(name="🥳 **Fun:**", value="``8ball, achievement, bird, cat, catfact, chatbot, dog, dogfact, fbi, hug, koalafact, norris, panda, pandafact, randomname, sentence, space, uwu, walter``", inline=False)
            embed.add_field(name="🛠️ **Moderation:**", value="``autorole[enable, disable, setrole], ban, clear, createrole, deleterole, lockdown[on, off], logs[enable(setting), disable(setting), setchannel, settings], mute, unban, unmute, role, softban``", inline=False)
            embed.add_field(name="📈 **Economy/Levels:**", value="``balance, buy, daily, fish, register, shop, stats``")
            embed.add_field(name="💎 **Miscellaneous:**", value="``botstats, changelog, complementary, google, hex, help, invite, serverinfo, source, suggestion, uptime, userinfo, wikipedia``", inline=False)
            embed.set_footer(text="WalterClementsBot - by MrHouck#2775 | v1.8.4")
            await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Help(client))
    now = datetime.now()
    print(f"{now} | Loaded help module.")
