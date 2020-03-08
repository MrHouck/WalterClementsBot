import discord
from discord.ext import commands
import discord.utils
import sqlite3
from datetime import datetime



#external logging is in place for muting and banning
class Logs(commands.Cog):
    def __init__(self, client):
        self.bot = client

    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    async def logs(self, ctx):
        if ctx.invoked_subcommand == None:
            await ctx.send('You need to specify a subcommand! (setchannel, enable, disable)')
    
    @logs.command(aliases=['sc', 'set', 'channel'])
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def setchannel(self, ctx, channel : discord.TextChannel=None):
        if channel == None:
            return await ctx.send('You need to specify a channel!')
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT channel_id, enabled FROM logs WHERE guild_id = '{ctx.guild.id}'") 
        result = cursor.fetchone()
        if result is None:
            sql = ("INSERT INTO logs(guild_id, channel_id, enabled) VALUES(?,?,?)")
            val = (ctx.guild.id, channel.id, "true")
            cursor.execute(sql, val)
            db.commit()
        elif result[0] == channel.id:
            return await ctx.send("Logs are already being written in this channel!")
        cursor.execute(f"UPDATE logs SET channel_id = '{channel.id}' WHERE guild_id = '{ctx.guild.id}'")
        db.commit()
        cursor.close()
        db.close()
        await ctx.send(f"Logs are now being recorded in {channel.mention}")

    @logs.command(aliases=['e', 'en'])
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def enable(self, ctx):
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT enabled FROM logs WHERE guild_id = {ctx.guild.id}")
        result = cursor.fetchone()
        if result == None:
            return await ctx.send("Logging is not set up!")
        elif result[0] == "true":
            return await ctx.send("Logging is already enabled!")
        else:
            cursor.execute(f"UPDATE logs SET enabled = 'true' WHERE guild_id = {ctx.guild.id}")
            db.commit()
            cursor.close()
            db.close()
            await ctx.send("Logging has been enabled.")

    @logs.command(aliases=['d', 'dis'])
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def disable(self, ctx):
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT enabled FROM logs WHERE guild_id = {ctx.guild.id}")
        result = cursor.fetchone()
        if result == None:
            return await ctx.send("Logging is not set up!")
        elif result[0] == "false":
            return await ctx.send("Logging is already disabled!")
        else:
            cursor.execute(f"UPDATE logs SET enabled = 'false' WHERE guild_id = {ctx.guild.id}")
            db.commit()
            cursor.close()
            db.close()
            await ctx.send("Logging has been disabled.")

    #------------------------#
    #                        #
    #       LISTENERS        #
    #                        #
    #------------------------#
    
    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload):
        if payload.cached_message.author.bot == True:
            return
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT channel_id, enabled FROM logs WHERE guild_id = {payload.guild_id}")
        result = cursor.fetchone()
        if result == None or result[1] == "false":
            return
        channelid = result[0]
        channel = self.bot.get_channel(int(channelid))
        await channel.send(f"`[({current_time})]` - **Message Deleted**\n```User: {payload.cached_message.author} (ID: {payload.cached_message.author.id})\nMessage: {payload.cached_message.content}``` ``Channel:`` {payload.cached_message.channel.mention}")

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.content == after.content:
            return
        if before.author.bot == True:
            return
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT channel_id, enabled FROM logs WHERE guild_id = {before.guild.id}")
        result = cursor.fetchone()
        if result == None or result[1] == "false":
            return
        channelid = result[0]
        channel = self.bot.get_channel(int(channelid))
        await channel.send(f"`[({current_time})]` - **Message Edited**\n```User: {before.author} (ID: {before.author.id})\nBefore: {before.content}\nAfter: {after.content}``` ``Channel:`` {before.channel.mention}")

    @commands.Cog.listener()
    async def on_member_leave(self, member):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT channel_id, enabled FROM logs WHERE guild_id = {before.guild.id}")
        result = cursor.fetchone()
        if result == None or result[1] == "false":
            return
        channelid = result[0]
        channel = self.bot.get_channel(int(channelid))
        await channel.send(f"`[({current_time})]` - **User Left Guild**\n`User: {member} (ID: {member.id})`")

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        guild_id = role.guild.id
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT channel_id, enabled FROM logs WHERE guild_id = {guild_id}")
        result = cursor.fetchone()
        if result == None or result[1] == "false":
            return
        channelid = result[0]
        channel = self.bot.get_channel(int(channelid))
        await channel.send(f"`[({current_time})]` - **Role Created**\n```Name: {role.name} (ID: {role.id})`\nHoist?: {role.hoist}\nPosition: {role.position}\nMentionable: {role.mentionable}\nColor: {role.color}```")
    


def setup(client):
    client.add_cog(Logs(client))
    now = datetime.now()
    print(f'{now} | Loaded logs module.')
