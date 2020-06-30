import discord
import wikipedia
import PIL
import time
import json
import math

import os
import random
import sqlite3
import urllib.request
from .resources.UrbanPy.urbandictionary import UrbanDictionary #self made api wrapper :o
from io import BytesIO
from PIL import Image
from googlesearch import search
from datetime import datetime
from discord.ext import commands
from urllib.request import urlopen
from textwrap import wrap
from urllib.parse import quote
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

class Misc(commands.Cog):
    def __init__(self, client):
        self.bot = client

    @commands.command(aliases=['uinfo', 'whois'], usage="[member]")
    @commands.guild_only()
    async def userinfo(self, ctx, member: discord.Member):
        """
        Get information on a user.
        """
        await ctx.trigger_typing()
        member = member if not None else ctx.author
        roles = [role for role in member.roles]
        embed = discord.Embed(colour=member.color, timestamp=ctx.message.created_at)
        embed.set_author(name=f"User info - {member}")
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        embed.add_field(name="User ID:", value=member.id, inline=False)
        embed.add_field(name="Current nickname:",value=member.display_name, inline=False)
        embed.add_field(name="Account created at:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"), inline=False)
        embed.add_field(name="Joined server at:", value=member.joined_at.strftime("%a, %#d %B %Y %I:%M %p UTC"), inline=False)
        embed.add_field(name=f"Roles ({len(roles)})", value=" ".join([role.mention for role in roles]), inline=False)
        embed.add_field(name="Top role:",value=member.top_role.mention, inline=False)
        embed.add_field(name="Bot?", value=member.bot, inline=False)
        await ctx.send(embed=embed)

    @commands.command(aliases=['sinfo','server'])
    @commands.guild_only()
    async def serverinfo(self, ctx):
        """
        Get information on the server you are in.
        """
        await ctx.trigger_typing()
        guild = ctx.guild
        embed = discord.Embed()
        embed.set_author(name=f"{guild}", icon_url=f"{guild.icon_url}")
        embed.add_field(name="Owner", value=f"{guild.owner.mention}", inline=True)
        embed.add_field(name="Region", value=f"{guild.region}", inline=True)
        embed.add_field(name="Categories",value=f"{len(guild.categories)}", inline=True)
        embed.add_field(name="Text Channels",value=f"{len(guild.text_channels)}", inline=True)
        embed.add_field(name="Voice Channels",value=f"{len(guild.voice_channels)}", inline=True)
        embed.add_field(name="Members", value=f"{guild.member_count}", inline=True)
        embed.add_field(name="Roles", value=f"{len(guild.roles)}", inline=True)
        embed.add_field(name="Verification Level", value=f"{guild.verification_level}", inline=True)
        embed.add_field(name="MFA Level", value=f"{guild.mfa_level}", inline=True)
        embed.add_field(name="Server boosters", value=f"{guild.premium_subscription_count}", inline=True)
        embed.add_field(name="Large", value=f"{guild.large}", inline=True)
        embed.add_field(name="Emoji Limit", value=f"{guild.emoji_limit}", inline=True)
        embed.add_field(name="Bitrate Limit", value=f"{guild.bitrate_limit}", inline=True)
        embed.add_field(name="File Size Limit", value=f"{guild.filesize_limit}", inline=True)
        embed.add_field(name="Icon URL", value=f"[URL]({guild.icon_url})", inline=True)
        embed.set_footer(text=f"Server ID: {guild.id} | {guild} was created at {guild.created_at.strftime('%a, %#d %B %Y, %I:%M %p UTC')}")
        await ctx.send(embed=embed)

    @commands.command(usage="<suggestion>")
    @commands.guild_only()
    async def suggestion(self, ctx, *, suggestion):
        """
        Send me a suggestion for this bot! Please note: usernames are recorded, you will be blacklisted if you abuse this feature.
        """
        await ctx.trigger_typing()
        with open('./config.json', 'r') as f:
            stuff = json.load(f)
        if ctx.author.id in stuff["blacklistedUsers"]:
            embed = discord.Embed(description="You have been permanently blacklisted from this command")
            return await ctx.send(embed=embed)

        user = self.bot.get_user(250067504641081355)
        sentId = ctx.author.id
        mention = f'<@{sentId}>'
        await user.send(f'{mention} | {suggestion}')
        embed = discord.Embed()
        embed.add_field(name="Thank you!", value="Your suggestion was sent successfully.", inline=True)
        await ctx.send(embed=embed)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def blacklistUser(self, ctx, user: discord.Member):
        """
        Blacklists a user from using +suggestion (bot owner only)
        """
        with open('./config.json', 'r') as f:
            stuff = json.load(f)
            f.close()
        stuff["blacklistedUsers"].append(user.id)
        with open('./config.json', 'w') as f:
            json.dump(stuff, f, indent=4)
            f.close()
        embed = discord.Embed(description=f"Permanently blacklisted {user.name}")
        return await ctx.send(embed=embed)
    
    @commands.command(usage="[version]")
    @commands.guild_only()
    async def changelog(self, ctx, version=None):
        """
        View the changelog for the bot.
        """

        await ctx.trigger_typing()
        with open(THIS_FOLDER+'/resources/changelog.json', 'r') as f:
            data = json.load(f)
            f.close()
        if version is None:
            message = "Valid versions are: `"
            for key in data:
                print(key)
                message += key+", "
            message = message[:-2]
            message += '`'
            return await ctx.send(message)
        if version not in data.keys():
            return await ctx.send(f"There is no update with that version!")
        embed = discord.Embed(title=f"Version {version} - {data[version]['date']}", color=0xff87f9)
        text=""
        for change in data[version]["changes"]:
            text+=f"{change}\n"
        embed.add_field(name="Changes:", value=text, inline=False)
        embed.add_field(name="That's all for now!", value="If you have any ideas or suggestions, lemme know by using the +suggestion command or just dming me!", inline=False)
        embed.set_footer(text=f"Version {version}")
        await ctx.send(embed=embed)
            
    @commands.command(aliases=['hex'], usage="<hexCode>")
    @commands.guild_only()
    async def visualizeHex(self, ctx, hexCode):
        """
        Get the color for a hex code.
        """
        await ctx.trigger_typing()
        if '#' in hexCode:
            hexCode = hexCode.replace('#', '')
        rgb = tuple(int(hexCode[i:i+2], 16) for i in (0, 2, 4))
        im = Image.new('RGB', (100, 100))
        for x in range(100):
            for y in range(100):
                im.putpixel((x, y), rgb)
        buffer = BytesIO()
        im.save(buffer, 'jpeg')
        buffer.seek(0)
        await ctx.send(f'``#{hexCode} - rgb{rgb}``')
        await ctx.send(file=discord.File(buffer, filename="color.png"))

    @commands.command(usage="<hexCode>")
    @commands.guild_only()
    async def complementary(self, ctx, hexCode):
        """
        Get the complementary color to a hex code color.
        """
        await ctx.trigger_typing()
        baseline = (255, 255, 255)
        if '#' in hexCode:
            hexCode = hexCode.replace('#', '')
        rgb = tuple(int(hexCode[i:i+2], 16) for i in (0, 2, 4))
        complementary = tuple(map(lambda i, j: i-j, baseline, rgb))
        im = Image.new('RGB', (100, 100))
        for x in range(100):
            for y in range(100):
                im.putpixel((x, y), complementary)
        buffer = BytesIO()
        im.save(buffer, 'jpeg')
        buffer.seek(0)
        await ctx.send(f'``Complementary color to #{hexCode} is {rgb}``')
        await ctx.send(file=discord.File(buffer, filename='complementary.png'))

    @commands.command(aliases=['wiki', 'article'], usage="<searchterm>")
    @commands.guild_only()
    async def wikipedia(self, ctx, *, searchterm):
        """
        Search wikipedia for whatever you want.
        """
        searchterm = searchterm.replace('@', '')
        try:
            page = wikipedia.page(searchterm, auto_suggest=False)
            summary = wikipedia.summary(searchterm, sentences=6)
        except wikipedia.DisambiguationError as e:
            s = e.options[0]
            page = wikipedia.page(s, auto_suggest=False)
            summary = wikipedia.summary(s, sentences=6)
        summary = summary + '...'
        url = page.url
        title = page.title
        if page.images != None:
            thumb = random.choice(page.images)
        embed = discord.Embed(title=f'{title}', url=f'{url}')
        embed.set_thumbnail(url=f"{thumb}")
        embed.add_field(name='Summary', value=f"{summary}")
        await ctx.send(embed=embed)

    @commands.command(aliases=['google', 'search'], usage="<query>")
    @commands.guild_only()
    async def google_search(self, ctx, *, query):
        """
        Get google search results for a query.
        """
        query = query.replace('@', '')
        embed = discord.Embed(title=f'Google Search results for: {query}')
        message = ''
        await ctx.send("Searching...")
        await ctx.trigger_typing()
        for result in search(query, tld='com', lang='en', num=5, stop=5, pause=1):
            embed.add_field(name='\u200b', value=f'[{result}]({result})', inline=False)
        await ctx.send(embed=embed)

    @commands.command(aliases=['urban', 'ud'], usage="[query]")
    @commands.guild_only()
    @commands.is_nsfw()
    async def urbandictionary(self, ctx, *, query=None):
        """
        Search a word on urban dictionary
        """
        urbanClient = UrbanDictionary()
        if query is None:
            query = "Random Word"
            term = urbanClient.define()
            term = term[0]
        else:
            query = query.replace('@', '')
            urlCompatible = query.replace(' ', '%20')
            term = urbanClient.define(urlCompatible)
            term = term[0]
        embed = discord.Embed(title=f'{query}', url=term.permalink, color=random.randint(1, 0xffffff))
        embed.add_field(name='Word', value=term.word)
        embed.add_field(name='Defintion', value=term.definition.replace('[','').replace(']',''), inline=False)
        embed.add_field(name='Example', value=term.example.replace('[','').replace(']',''), inline=False)
        embed.add_field(name='Thumbs Up | Thumbs Down', value=f'{term.thumbs_up} | {term.thumbs_down}', inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def ping(self, ctx):
        """
        Gets the client latency. (The ping of the bot)
        """
        await ctx.trigger_typing()
        embed = discord.Embed(title="Pong!", color=0xff8040)
        embed.add_field(name="Client Latency:", value=f"{round(self.bot.latency * 1000)}ms", inline=False)
        embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(hidden=True)
    @commands.is_owner()
    @commands.guild_only()
    async def logout(self, ctx):
        """
        Shut down the bot (Bot owner only).
        """
        await ctx.trigger_typing()
        if ctx.author.id == 250067504641081355:
            await ctx.send('🔋 | Shutting down...')
            await self.bot.logout()
        else:
            await ctx.send('404 Gateway Not Found')

    @commands.command()
    async def invite(self, ctx):
        """
        Get the invite link for the bot.
        """
        embed = discord.Embed(title='Invite me!',url="https://mrhouck.github.io/walter/")
        embed.add_field(name="Join the support server", value="https://discord.gg/gP2AgXN")
        await ctx.send(embed=embed)

    @commands.command()
    async def source(self, ctx):
        """
        View the source code for the bot.
        """
        embed = discord.Embed(
            title='Source Code', url="https://github.com/MrHouck/WalterClementsBot")
        embed.set_footer(text="i know my code is terrible")
        await ctx.send(embed=embed)

    @commands.command(aliases=['random', 'randint', 'randomnum'], usage="<lower> <upper>")
    async def rand(self, ctx, lower:int, upper:int):
        """
        Generate a random number in a range.
        """
        await ctx.trigger_typing()
        if lower > upper:
            return await ctx.send("The `lower` value cannot be higher than the `upper` value.")
        embed = discord.Embed(title='Random Number Generator', color=random.randint(1, 0xffffff))
        rand = random.randint(lower, upper)
        embed.add_field(name=f'Random number between {lower} and {upper}', value=str(rand))
        return await ctx.send(embed=embed)

    @commands.command(hidden=True, usage="<toExecute>")
    @commands.is_owner()
    async def sql(self, ctx, *, toExecute):
        """
        Execute an sqlite3 command (bot owner only)
        """
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        try:
            cursor.execute(toExecute)
            if 'SELECT' in toExecute:
                msg = ""
                if 'SELECT *' in toExecute:
                    result = cursor.fetchall()
                    for r in result:
                        msg += "\n{}".format(r)
                else:
                    result = cursor.fetchone()
                    for r in result:
                        msg += "\n{}".format(r)
                return await ctx.send(f"```{msg}```")
            else:
                db.commit()
                cursor.close()
                db.close()
                return await ctx.send("done")
        except Exception as e:
            return await ctx.send(e)

    @commands.command(aliases=['e', 'emote'], usage="<emoji>")
    @commands.guild_only()
    async def emoji(self, ctx, emoj: discord.Emoji):
        """
        View a custom emoji.
        """
        embed = discord.Embed(color=random.randint(1, 0xffffff), title=emoj.name)
        emojiUrl="https://cdn.discordapp.com/emojis/{}.png?v=1".format(emoj.id)
        embed.set_image(url=emojiUrl)
        return await ctx.send(embed=embed)

    



def setup(client):
    client.add_cog(Misc(client))
    now = datetime.now()
    print(f'{now} | Loaded misc module.')
