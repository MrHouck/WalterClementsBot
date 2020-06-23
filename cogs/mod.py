import discord
import asyncio
from datetime import datetime, timedelta
from discord.ext import commands
from discord.utils import get
from collections.abc import Sequence
import random #for random embed colors
import sqlite3
blacklistedUsers = []

class Mod(commands.Cog):
    def __init__(self, client):
        self.bot = client

    @commands.command(usage="<member> [reason]")
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        """
        Kick a member.
        """ 
        if reason is None:
            reason="None"
        await ctx.trigger_typing()
        await member.kick(reason=reason)
        await ctx.send(f'{member.mention} kicked by {ctx.author}. [{reason}]')

    @commands.command(usage="<member> [reason]")
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        """
        Ban a member.
        """
        if reason is None:
            reason = "None"
        await ctx.trigger_typing()
        await member.ban(reason=reason)
        embed=discord.Embed(title="Success!", color=0x008000)
        embed.add_field(name="Banned User:", value=f"{member}", inline=False)
        embed.add_field(name="Reason:", value=f"{reason}", inline=False)
        embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

        #for logs
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT channel_id, memberBanned FROM logs WHERE guild_id = '{ctx.guild.id}'")
        result = cursor.fetchone()
        if result == None:
            return
        if result[1] == 0:
            return
        else:
            time = datetime.now()
            current_time = time.strftime("%H:%M:%S")
            channel = self.bot.get_channel(int(result[0]))
            message = f"[({current_time})] - **Member Banned**\n```User {member} (ID: {member.id})\nBanned by: {ctx.author} (ID: {ctx.author.id})\nReason: {reason}```"
            await channel.send(message)

    @commands.command(aliases=['purge'], usage="<amount>")
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        """
        Purge an amount of messages in a channel.
        """
        await ctx.trigger_typing()
        await ctx.channel.purge(limit=amount + 1)
        embed = discord.Embed()
        embed.add_field(name=f"Purged {amount} messages", value=f"Channel: #{ctx.channel}", inline=False)
        embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed, delete_after=5)

    @commands.command(usage="<member> <role>")
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    async def role(self, ctx, member : discord.Member, *, role):
        """
        Give someone a role or remove it if they already have it.
        """
        await ctx.trigger_typing()
        guild = ctx.guild
        message = ctx.message
        emoji = '\N{THUMBS UP SIGN}'
        role = get(guild.roles, name=role)
        if role == None:
                embed = discord.Embed(color=0xff2d2d)
                embed.add_field(name="Error:", value=f"Role does not exist.", inline=False)
                embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
        else:
            if role in member.roles:
                await member.remove_roles(role)
                await message.add_reaction(emoji)
                await ctx.send(f"Removed {role} from {member.mention}")
            else:
                await member.add_roles(role)
                await message.add_reaction(emoji)
                await ctx.send(f"Added {role} to {member.mention}")

    @commands.command(usage="<member> [reason]")
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def softban(self, ctx, member : discord.Member, *, reason=None):
        """
        Ban a user then instantly unban them. Equivalent to a kick, but removes all their messages.
        """
        if reason is None:
            reason = "None"
        await ctx.trigger_typing()
        await member.ban(reason=reason)
        banned_users = await ctx.guild.bans()
        await ctx.guild.unban(member)
        await ctx.send(f"Softbanned {member}.\nNote that this means they can rejoin.")

    @commands.command(usage="<member>")
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        """
        Unban someone who was banned.
        """
        await ctx.trigger_typing()
        if member is not discord.Member:
            banned_users = await ctx.guild.bans()
            member_name, member_discriminator = member.split('#')
        else:
            member_name = member.name
            member_discriminator = member.discriminator
        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                embed=discord.Embed(title="Success!", color=0x008000)
                embed.add_field(name="Unbanned user:", value=f"{user.name}#{user.discriminator}", inline=False)
                embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
        ##for logs
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT channel_id, memberBanned FROM logs WHERE guild_id = '{ctx.guild.id}'")
        result = cursor.fetchone()
        if result == None:
            return
        if result[1] == 0:
            return
        else:
            time = datetime.now()
            current_time = time.strftime("%H:%M:%S")
            channel = self.bot.get_channel(int(result[0]))
            message = f"[({current_time})] - **Member Unbanned**\n```User {member} (ID: {member.id})\nUnbanned by: {ctx.author} (ID: {ctx.author.id})```"
            await channel.send(message)


    @commands.command(aliases=['addrole'], usage="[rolename] [rolecolor] [hoist] [mentionable] [reason]")
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    async def createrole(self, ctx, rolename="new role", color="#000000", hoist=False, mentionable=True, reason="None"):
        """
        Create a role.
        """
        original = color
        color = color.strip('#')
        colorlen = len(color)
        color = tuple(int(color[i:i+colorlen/3], 16) for i in range(0, colorlen, colorlen/3))
        color = discord.Color.from_rgb(color)
        await ctx.trigger_typing()
        guild = ctx.guild
        await guild.create_role(name=rolename, colour=color, hoist=hoist, mentionable=mentionable, reason=reason)
        embed=discord.Embed(title="Success!", color=color)
        embed.add_field(name="Created new role:", value=f"{rolename}­", inline=False)
        embed.add_field(name="Properties:", value=f"Color: {color}\nHoist: {hoist}\nMentionable: {mentionable}\nReason: {reason}", inline=False)
        embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(aliases=['delrole', 'removerole'], usage="<rolename> [reason]")
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    async def deleterole(self, ctx, role: discord.Role, *, reason=None):
        """
        Delete a role. Note: To remove a role with spaces in it, you must put the role in quotations.
        """
        if reason is None:
            reason = "None."
        await ctx.trigger_typing()
        if role==None:
            embed=discord.Embed(color=0xff2d2d)
            embed.add_field(name="Error", value="You must specify a role to delete.", inline=True)
            embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        guild = ctx.guild
        try:
            embe=discord.Embed(title="Success!", color=0x008000)
            embe.add_field(name=f"The role {role} was deleted", value=f"Reason: {reason}", inline=False)
            embe.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
            await role.delete(reason=reason)
            await ctx.send(embed=embe)
        except discord.Forbidden:
            emb=discord.Embed(color=0xff2d2d)
            emb.add_field(name="Error", value="I am missing permissions!", inline=True)
            emb.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=emb)
def setup(client):
    client.add_cog(Mod(client))
    now = datetime.now()
    print(f'{now} | Loaded moderation module.')