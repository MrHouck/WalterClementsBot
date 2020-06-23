import discord
import asyncio
from datetime import datetime, timedelta
import time
from discord.ext import commands, tasks
from discord.utils import get
from collections.abc import Sequence
import random #for random embed colors
import sqlite3
class Mute(commands.Cog):
    def __init__(self, client):
        self.bot = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        self.poll_mutes.start()
    @commands.command(usage="<member> <time> [reason]")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def mute(self, ctx, member : discord.Member, length='inf', *, reason="None"):
        """
        Mute a user.
        """
        await ctx.trigger_typing()
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()

        current_time = int(time.time())
        datetime_obj = datetime.fromtimestamp(current_time)
        if length.endswith('m'):
            if int(length.replace('m','')) < 1:
                return await ctx.send("The minimum mute time is 1 minute.")
            unmuteTime = datetime_obj + timedelta(minutes=int(length.replace('m', '')))
        elif length.endswith('h'):
            unmuteTime = datetime_obj + timedelta(hours=int(length.replace('h', '')))
        elif length.endswith('d'):
            unmuteTime = datetime_obj + timedelta(hours=int(length.replace('d', '')))
        elif length == 'inf':
            unmuteTime = datetime_obj + timedelta(weeks=52142) #1000 years 
        else:
            return await ctx.send("Invalid unit of time! Some examples of accepted forms of time is `24h, 2m, 4d, 19h`")
        user_id = member.id
        guild = ctx.guild
        role = get(guild.roles, name="Muted")
        if role:
            cursor.execute(f"SELECT user_id FROM mutes WHERE guild_id = {guild.id}")
            result = cursor.fetchone()
            if result:
                embed = discord.Embed(color=0xff2d2d)
                embed.add_field(name="Error:", value=f"{member} is already muted. Perhaps you meant to unmute them?", inline=False)
                embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
            elif role in member.roles:        
                embed = discord.Embed(color=0xff2d2d)
                embed.add_field(name="Error:", value=f"{member} already has the muted role. To mute them, you need to remove it.", inline=False)
                embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
            else:
                sql=("INSERT INTO mutes(guild_id, user_id, endtime) VALUES(?, ?, ?)")
                val=(guild.id, user_id, unmuteTime)
                cursor.execute(sql, val)
                db.commit()

                await member.add_roles(role)
                embed=discord.Embed()



                #Log-related
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                logMessage = f"``[({current_time})]`` - **User Muted**"
                logMessage += f"```User: {member} (ID: {member.id})"
                
                embed.set_author(name=f"Muted: {member}", icon_url=member.avatar_url)
                embed.add_field(name="Reason:", value=f"{reason}", inline=True)
                if length.endswith('s'):
                    embed.add_field(name="Time:", value=f'{length.replace("s", "")} seconds', inline=True)
                    logMessage += f"\nLength: {length.replace('s', '')} seconds"
                elif length.endswith('m'):
                    embed.add_field(name="Time:", value=f'{length.replace("m", "")} minutes', inline=True)
                    logMessage += f"\nLength: {length.replace('m', '')} minutes"
                elif length.endswith('h'):
                    embed.add_field(name="Time:", value=f'{length.replace("h", "")} hours', inline=True)
                    logMessage += f"\nLength: {length.replace('h', '')} hours"
                elif length.endswith('d'):
                    embed.add_field(name="Time:", value=f'{length.replace("d", "")} days', inline=True)
                    logMessage += f"\nLength: {length.replace('d', '')} days"
                else:
                    embed.add_field(name="Time:", value=f'Permanent', inline=True)
                    logMessage += "\nLength: Permanent"

                logMessage += f"\nReason: {reason}```"

                embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)


                cursor.execute(f"SELECT channel_id, enabled, memberMuted FROM logs WHERE guild_id = '{guild.id}'")
                result = cursor.fetchone()
                if result == None:
                    pass
                elif result[1] == 'false':
                    pass
                elif result[2] == 0:
                    pass
                else:
                    channelid = result[0]
                    channel = self.bot.get_channel(int(channelid))
                    await channel.send(logMessage)
                    cursor.close()
                    db.close()

        else:
            await ctx.send("The muted role is not set up! Creating and adding to the user now...")
            guild = ctx.guild
            await guild.create_role(name='Muted', color=discord.Colour.dark_grey(), hoist=False, mentionable=False, reason='Configuring the muted role.')
            role = get(guild.roles, name="Muted")
            await role.edit(position=1)
            overwrite = discord.PermissionOverwrite()
            overwrite.send_messages = False
            overwrite.add_reactions = False
            overwrite.speak = False
            for category in guild.categories:
                try:
                    await category.set_permissions(role, overwrite=overwrite)
                except:
                    pass
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
        cursor.execute(f"SELECT channel_id, enabled, memberMuted FROM logs WHERE guild_id = '{guild.id}'")
        result = cursor.fetchone()
        channel=None
        if result is None:
            pass
        elif result[1] == 'false':
            pass
        elif result[2] == 0:
            pass
        else:
            channel = self.bot.get_channel(int(result[0]))
        now = datetime.now()

        current_time = now.strftime("%H:%M:%S")
        logMessage = f"``[({current_time})]`` - **User Unmuted**"
        logMessage += f"```User: {member} (ID: {member.id})"
        logMessage += f"\nUnmuted by: {ctx.author} (ID: {ctx.author.id})"
        logMessage += f"\nReason: {reason}```"

        cursor.execute(f"SELECT * FROM mutes WHERE guild_id={guild.id} AND user_id={member.id}")
        result = cursor.fetchone()
        role = get(guild.roles, name="Muted")
        
        if role in member.roles and result:
            await member.remove_roles(role)
            
            embed=discord.Embed()
            embed.set_author(name=f"Unmuted: {member}", icon_url=member.avatar_url)
            embed.add_field(name="Reason:", value=f"{reason}", inline=False)
            embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
            
            cursor.execute(f"DELETE FROM mutes WHERE guild_id ={guild.id} AND user_id={member.id}")
            db.commit()
            cursor.close()
            db.close()
            
            await ctx.send(embed=embed)
            if channel:
                await channel.send(logMessage)
        
        elif not role in member.roles and result:
            
            embed=discord.Embed()
            embed.set_author(name=f"Unmuted: {member}", icon_url=member.avatar_url)
            embed.add_field(name="Reason:", value=f"{reason}", inline=False)
            embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
            
            cursor.execute(f"DELETE FROM mutes WHERE guild_id ={guild.id} AND user_id={member.id}")
            db.commit()
            cursor.close()
            db.close()
            
            await ctx.send(embed=embed)
            if channel:
                await channel.send(logMessage)
        else:
            return await ctx.send("That member is not muted.")


    @tasks.loop(seconds=5)
    async def poll_mutes(self):
        try:
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()
            cursor.execute("SELECT * FROM mutes")
            mutes = cursor.fetchall()
            for mute in mutes:
                endTime = mute[2]
                endTimeObj = datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S')
                currentTime = datetime.now()
                if currentTime > endTimeObj:
                    guild_id = mute[0]
                    guild = self.bot.get_guild(int(guild_id))
                    role = get(guild.roles, name="Muted")
                    if not role:
                        pass
                    user = guild.get_member(int(mute[1]))
                    if role in user.roles:
                        await user.remove_roles(role)
                        cursor.execute(f"DELETE FROM mutes WHERE guild_id={guild_id} AND user_id={user.id}")
                        db.commit()
                        cursor.execute(f"SELECT channel_id, enabled, memberMuted FROM logs WHERE guild_id = {guild.id}")
                        result = cursor.fetchone()
                        if not result:
                            pass
                        elif result[1] == 'true' and result[2] == 1:
                            currentTime = currentTime.strftime("%H:%M:%S")
                            logMessage = f"``[({current_time})]`` - **User Unmuted**"
                            logMessage += f"```User: {member} (ID: {member.id})"
                            logMessage += f"\nReason: Automatic```"
                            await channel.send(logMessage)
        except Exception as e:
            print(e)
                
                



    
def setup(client):
    client.add_cog(Mute(client))
    now = datetime.now()
    print(f'{now} | Loaded mute module.')