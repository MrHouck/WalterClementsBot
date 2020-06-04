import discord
import asyncio
from datetime import datetime, timedelta
from discord.ext import commands
from discord.utils import get
from collections.abc import Sequence
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

    @commands.command(usage="<member> <time> [reason]")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def mute(self, ctx, member : discord.Member, time, *, reason=None):
        """
        Mute a user.
        """
        if reason is None:
            reason = "None"
        await ctx.trigger_typing()
        s = False
        m = False
        h = False
        d = False
        if 's' in time:
            s = True
            time = time.replace('s', '')
        elif 'm' in time:
            m = True
            time = time.replace('m', '')
        elif 'h' in time:
            h = True
            time = time.replace('h', '')
        elif 'd' in time:
            d = True
            time = time.replace('d', '')
        else:
            return await ctx.send("That isn't a valid unit of time! The valid units are: `s, m, h, d`")
        user_id = member.id
        guild = ctx.guild
        time = int(time)
        role = get(guild.roles, name="Muted")
        if role:
            if role in member.roles:
                embed = discord.Embed(color=0xff2d2d)
                embed.add_field(name="Error:", value=f"{member} is already muted. Perhaps you meant to unmute them?", inline=False)
                embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
            else:
                await member.add_roles(role)
                embed=discord.Embed()

                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                logMessage = f"``[({current_time})]`` - **User Muted**"
                logMessage += f"```User: {member} (ID: {member.id})"
                
                embed.set_author(name=f"Muted: {member}", icon_url=member.avatar_url)
                embed.add_field(name="Reason:", value=f"{reason}", inline=True)
                if s == True:
                    embed.add_field(name="Time:", value=f'{time} seconds', inline=True)
                    logMessage += f"\nLength: {time} seconds"
                elif m == True:
                    embed.add_field(name="Time:", value=f'{time} minutes', inline=True)
                    logMessage += f"\nLength: {time} minutes"
                elif h == True:
                    embed.add_field(name="Time:", value=f'{time} hours', inline=True)
                    logMessage += f"\nLength: {time} hours"
                elif d == True:
                    embed.add_field(name="Time:", value=f'{time} days', inline=True)
                    logMessage += f"\nLength: {time} days"
                logMessage += f"\nReason: {reason}```"

                embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)


                db = sqlite3.connect('main.sqlite')
                cursor = db.cursor()
                cursor.execute(f"SELECT channel_id, memberMuted FROM logs WHERE guild_id = '{guild.id}'")
                result = cursor.fetchone()
                if result == None:
                    pass
                elif result[1] == 0:
                    pass
                else:
                    channelid = result[0]
                    channel = self.bot.get_channel(int(channelid))
                    await channel.send(logMessage)


                if s == True:
                    await asyncio.sleep(time)
                    await member.remove_roles(role, reason='Mute expired')
                elif m == True:
                    await asyncio.sleep(time * 60)
                    await member.remove_roles(role, reason='Mute expired')
                elif h == True:
                    await asyncio.sleep(time * (60**2))
                    await member.remove_roles(role, reason='Mute expired')
                elif d == True:
                    await asyncio.sleep(time * (60**2) * 24)
                    await member.remove_roles(role, reason='Mute')
                else:
                    return await ctx.send('There was an error setting the time for the mute.')
                
                if result == None:
                    return
                elif result[1] == 0:
                    return
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                logMessage = f"``[({current_time})]`` - **User Unmuted**"
                logMessage += f"```User: {member} (ID: {member.id})"
                logMessage += f"\nReason: Automatic```"
                await channel.send(logMessage)
        else:
            await ctx.send("The muted role is not set up! Creating and adding to the user now...")
            guild = ctx.guild
            await guild.create_role(name='Muted', color=discord.Colour.dark_grey(), hoist=False, mentionable=False, reason='Configuring the muted role.')
            role = get(guild.roles, name="Muted")
            perms = discord.Permissions(send_messages=False)
            await role.edit(permissions=perms)
            await role.edit(position=5)
            for channel in guild.channels:
                await channel.set_permissions(role, send_messages=False)
            await member.add_roles(role)


    @commands.command(usage="<member> [reason]")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def unmute(self, ctx, member : discord.Member, *, reason=None):
        """
        Unmute someone who is muted.
        """
        if reason is None:
            reason = "None"
        await ctx.trigger_typing()
        guild = ctx.guild
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT channel_id, memberMuted FROM logs WHERE guild_id = '{guild.id}'")
        result = cursor.fetchone()
        if result == None:
            return
        elif result[1] == 0:
            return
        else:
            channel = self.bot.get_channel(int(result[0]))
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        logMessage = f"``[({current_time})]`` - **User Unmuted**"
        logMessage += f"```User: {member} (ID: {member.id})"
        logMessage += f"\nUnmuted by: {ctx.author} (ID: {ctx.author.id})"
        logMessage += f"\nReason: {reason}```"

        role = get(guild.roles, name="Muted")
        if role in member.roles:
            await member.remove_roles(role)
            embed=discord.Embed()
            embed.set_author(name=f"Unmuted: {member}", icon_url=member.avatar_url)
            embed.add_field(name="Reason:", value=f"{reason}", inline=False)
            embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            await channel.send(logMessage)
        else:
            embed=discord.Embed(color=0xff2d2d)
            embed.add_field(name="Error:", value=f"{member} is not muted. Perhaps you meant to mute them?", inline=False)
            embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

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
    async def deleterole(self, ctx, rolename=None, *, reason=None):
        """
        Delete a role. Note: To remove a role with spaces in it, you must put the role in quotations.
        """
        if reason is None:
            reason = "None."
        await ctx.trigger_typing()
        if rolename==None:
            embed=discord.Embed(color=0xff2d2d)
            embed.add_field(name="Error", value="You must specify a role to delete.", inline=True)
            embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        guild = ctx.guild
        role = get(guild.roles, name=rolename)
        if role:
            try:
                embe=discord.Embed(title="Success!", color=0x008000)
                embe.add_field(name=f"The role {role} was deleted", value=f"Reason: {reason}", inline=False)
                embe.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
                await role.delete(reason=reason)
                await ctx.send(embed=embe)
            except discord.Forbidden:
                emb=discord.Embed(color=0xff2d2d)
                emb.add_field(name="Error", value="You are missing permissions!", inline=True)
                emb.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=emb)
        else:
            em=discord.Embed(color=0xff2d2d)
            em.add_field(name="Error", value="The role you attempted to delete does not exist.", inline=False)
            em.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=em)

    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    async def autorole(self, ctx):
        """
        Base command for autorole.
        """
        if ctx.invoked_subcommand == None:
            return await ctx.send('You need to specify a subcommand! (enable, disable, setrole)')

    @autorole.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def setrole(self, ctx, *, role):
        """
        Set the role that is to be automatically assigned when a user joins.
        """
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        guild = ctx.guild
        cursor.execute(f"SELECT enabled, role FROM autorole WHERE guild_id = '{guild.id}'")
        result = cursor.fetchone()
        if result == None:
            sql = ("INSERT INTO autorole(guild_id, role, enabled) VALUES(?,?,?)")
            val = (guild.id, role, "true")
            cursor.execute(sql, val)
            db.commit()
        elif get(guild.roles, name=role) == get(guild.roles, name=result[1]):
            return await ctx.send("This role is already being automatically assigned!")
        else:
            role = get(guild.roles, name=role)
            if role == None:
                return await ctx.send('This role does not exist!')
            cursor.execute(f"UPDATE autorole SET role = '{role}' WHERE guild_id = '{guild.id}'")
            db.commit()
            cursor.close()
            db.close()
            return await ctx.send(f"The new autorole for this server is now {role}.")

    @autorole.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def disable(self, ctx):
        """
        Disable the autorole module.
        """
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        guild = ctx.guild
        cursor.execute(f"SELECT enabled FROM autorole WHERE guild_id = '{guild.id}'")
        result = cursor.fetchone()
        if result == None:
            return await ctx.send("``Autorole`` has not been setup yet!")
        elif result == "false":
            return await ctx.send("``Autorole`` is already disabled!")
        else:
            cursor.execute(f"UPDATE autorole SET enabled = 'false' WHERE guild_id = '{guild.id}'")
            db.commit()
            cursor.close()
            db.close()
    
    @autorole.command()
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def enable(self, ctx):
        """
        Enable the autorole module.
        """
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        guild = ctx.guild
        cursor.execute(f"SELECT enabled FROM autorole WHERE guild_id = '{guild.id}'")
        result = cursor.fetchone()
        if result == None:
            return await ctx.send("``Autorole`` has not been setup yet!")
        elif result == "true":
            return await ctx.send("``Autorole`` is already enabled!")
        else:
            cursor.execute(f"UPDATE autorole SET enabled = 'true' WHERE guild_id = '{guild.id}'")
            db.commit()
            cursor.close()
            db.close()

def setup(client):
    client.add_cog(Mod(client))
    now = datetime.now()
    print(f'{now} | Loaded moderation module.')