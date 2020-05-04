import discord
from io import BytesIO
import wikipedia
import PIL
from PIL import Image
from googlesearch import search
import urbandict
import urllib.request
import time
import json
from datetime import datetime
import random
from discord.ext import commands


class Misc(commands.Cog):
    def __init__(self, client):
        self.bot = client

    @commands.command(aliases=['uinfo', 'whois'])
    @commands.guild_only()
    async def userinfo(self, ctx, member: discord.Member):
        await ctx.trigger_typing()
        """
        Get a users ID, nickname, account creation date, server join date, roles, and top role. Also checks if they are a bot.
        """
        roles = [role for role in member.roles]
        embed = discord.Embed(colour=member.color,
                              timestamp=ctx.message.created_at)
        embed.set_author(name=f"User info - {member}")
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(
            text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        embed.add_field(name="User ID:", value=member.id, inline=False)
        embed.add_field(name="Current nickname:",
                        value=member.display_name, inline=False)

        embed.add_field(name="Account created at:", value=member.created_at.strftime(
            "%a, %#d %B %Y, %I:%M %p UTC"), inline=False)
        embed.add_field(name="Joined server at:", value=member.joined_at.strftime(
            "%a, %#d %B %Y %I:%M %p UTC"), inline=False)

        embed.add_field(name=f"Roles ({len(roles)})", value=" ".join(
            [role.mention for role in roles]), inline=False)
        embed.add_field(name="Top role:",
                        value=member.top_role.mention, inline=False)

        embed.add_field(name="Bot?", value=member.bot, inline=False)

        await ctx.send(embed=embed)

    @commands.command(aliases=['sinfo'])
    @commands.guild_only()
    async def serverinfo(self, ctx):
        await ctx.trigger_typing()
        """
        Get information on a server, like its owner, id, region, creation date, category count, text channel count, voice channel count, member count, and role count.
        """
        guild = ctx.guild
        embed = discord.Embed()
        embed.set_author(name=f"{guild}", icon_url=f"{guild.icon_url}")
        embed.add_field(name="Owner", value=f"{guild.owner}", inline=True)
        embed.add_field(name="Region", value=f"{guild.region}", inline=True)
        embed.add_field(name="Categories",
                        value=f"{len(guild.categories)}", inline=True)
        embed.add_field(name="Text Channels",
                        value=f"{len(guild.text_channels)}", inline=True)
        embed.add_field(name="Voice Channels",
                        value=f"{len(guild.voice_channels)}", inline=True)
        embed.add_field(
            name="Members", value=f"{guild.member_count}", inline=True)
        embed.add_field(name="Roles", value=f"{len(guild.roles)}", inline=True)
        embed.set_footer(
            text=f"Server ID: {guild.id} | {guild} was created at {guild.created_at.strftime('%a, %#d %B %Y, %I:%M %p UTC')}")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def suggestion(self, ctx, *, suggestion):
        await ctx.trigger_typing()
        user = self.bot.get_user(250067504641081355)
        sentId = ctx.author.id
        mention = f'<@{sentId}>'
        await user.send(f'{mention} | {suggestion}')
        await user.send(suggestion)
        embed = discord.Embed()
        embed.add_field(
            name="Thank you!", value="Your suggestion was sent successfully.", inline=True)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def changelog(self, ctx):
        await ctx.trigger_typing()
        embed = discord.Embed(title="v1.8.5", color=0xff80ff)
        embed.add_field(
            name="Commands: ", value="Added ``+jackbox`` and probably more i'm forgetting", inline=False)
        embed.add_field(name="Fixes/Changes: ", value="- bug fixes\n- Added jackbox command, allows you to post a jackbox announcement in a channel that auto-updates with the players and audience count.\n-- SPECIFIC TO THIS SERVER-- there is a new channel where you can type a sentence and it'll add it to a text document which will get uploaded to a text file hosted at ziad87.me/paragraph.txt - try it out.", inline=False)
        embed.add_field(name="That's all for now!",
                        value="If you have any ideas or suggestions, lemme know by using the +suggestion command or just dming me!", inline=False)
        embed.set_footer(text="v1.8.4")
        await ctx.send(embed=embed)

    @commands.command(aliases=['hex'])
    @commands.guild_only()
    async def visualizeHex(self, ctx, hexCode):
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

    @commands.command()
    @commands.guild_only()
    async def complementary(self, ctx, hexCode):
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

    @commands.command(aliases=['wiki', 'article'])
    @commands.guild_only()
    async def wikipedia(self, ctx, *, searchterm):
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

    @commands.command(aliases=['google', 'search'])
    @commands.guild_only()
    async def google_search(self, ctx, *, query):
        query = query.replace('@', '')
        embed = discord.Embed(title=f'Google Search results for: {query}')
        message = ''
        await ctx.send("Searching...")
        await ctx.trigger_typing()
        for result in search(query, tld='com', lang='en', num=5, stop=5, pause=1):
            embed.add_field(
                name='\u200b', value=f'[{result}]({result})', inline=False)
        await ctx.send(embed=embed)

    @commands.command(aliases=['urban', 'ud'])
    @commands.guild_only()
    async def urbandictionary(self, ctx, *, query):
        query = query.replace('@', '')
        url_search = query.replace(' ', '%20')
        definition = urbandict.define(query)
        embed = discord.Embed(
            title=f'{query}', url=f'https://urbandictionary.com/define.php/term?={url_search}')
        embed.add_field(name='Word', value=definition[0]['word'])
        embed.add_field(name='Defintion', value=definition[0]['def'])
        print(definition[0]['example'])
        embed.add_field(name='Example', value=definition[0]['example'])
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def ping(self, ctx):
        """
        Gets the client latency. (The ping of the bot)
        """
        await ctx.trigger_typing()
        embed = discord.Embed(title="Pong!", color=0xff8040)
        embed.add_field(name="Client Latency:",
                        value=f"{round(self.bot.latency * 1000)}ms", inline=False)
        embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    @commands.guild_only()
    async def logout(self, ctx):
        await ctx.trigger_typing()
        if ctx.author.id == 250067504641081355:
            await ctx.send('🔋 | Shutting down...')
            await self.bot.logout()
        else:
            await ctx.send('404 Gateway Not Found')

    @commands.command()
    async def invite(self, ctx):
        embed = discord.Embed(title='Invite me!',
                              url="https://mrhouck.github.io/walterbot/")
        await ctx.send(embed=embed)

    @commands.command()
    async def source(self, ctx):
        embed = discord.Embed(
            title='Source Code', url="https://github.com/MrHouck/WalterClementsBot")
        embed.set_footer(text="i know my code is terrible")
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Misc(client))
    now = datetime.now()
    print(f'{now} | Loaded misc module.')
