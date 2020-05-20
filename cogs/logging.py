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
        """
        Base command for the logging module.
        """
        if ctx.invoked_subcommand == None:
            await ctx.send('You need to specify a subcommand! (enable[setting], disable[setting], setchannel, settings)')
    
    @logs.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def disable(self, ctx, *, setting):
        """
        Disable logging a specified action.
        """
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT roleCreated, roleDeleted, memberBanned, memberMuted, messageEdit, messageDelete, memberLeave, memberJoin, channelDelete, channelCreate, bulkMessageDelete FROM logs WHERE guild_id = {ctx.guild.id}")
        settings = cursor.fetchone()
        if setting.lower() == "role created" or setting.lower() == "role creation":
            if settings[0] == 0:
                return await ctx.send(f'Logging ``role creation`` is already disabled!')
            cursor.execute(f"UPDATE logs SET roleCreated = 0 WHERE guild_id = {ctx.guild.id}")
            await ctx.send("Logging ``role creation`` is now disabled.")
            db.commit()
            cursor.close()
            db.close()
        elif setting.lower() == "role deleted" or setting.lower() == "role deletion":
            if settings[1] == 0:
                return await ctx.send(f'Logging ``role deletion`` is already disabled!')
            cursor.execute(f"UPDATE logs SET roleDeleted = 0 WHERE guild_id = {ctx.guild.id}")
            await ctx.send("Logging ``role deletion`` is now disabled.")
            db.commit()
            cursor.close()
            db.close()
        elif setting.lower() == "member banned" or setting.lower() == "member banning" or setting.lower() == "member unbanning" or setting.lower() == "member banning/unbanning":
            if settings[2] == 0:
                return await ctx.send(f'Logging ``member banning/unbanning`` is already disabled!')
            cursor.execute(f"UPDATE logs SET memberBanned = 0 WHERE guild_id = {ctx.guild.id}")
            await ctx.send("Logging ``member banning/unbanning`` is now disabled.")
            db.commit()
            cursor.close()
            db.close()
        elif setting.lower() == "member muted" or setting.lower() == "member muting" or setting.lower() == "member unmuting" or setting.lower() == "member muting/unmuting":
            if settings[3] == 0:
                return await ctx.send(f'Logging ``member muting/unmuting`` is already disabled!')
            cursor.execute(f"UPDATE logs SET memberMuted = 0 WHERE guild_id = {ctx.guild.id}")
            await ctx.send("Logging ``member muting/unmuting`` is now disabled.")
            db.commit()
            cursor.close()
            db.close()
        elif setting.lower() == "message edited" or setting.lower() == "message edits":
            if settings[4] == 0:
                return await ctx.send(f'Logging ``message edits`` is already disabled!')
            cursor.execute(f"UPDATE logs SET messageEdit = 0 WHERE guild_id = {ctx.guild.id}")
            await ctx.send("Logging ``message edits`` is now disabled.")
            db.commit()
            cursor.close()
            db.close()
        elif setting.lower() == "message deleted" or setting.lower() == "message deletion":
            if settings[5] == 0:
                return await ctx.send(f'Logging ``message deletion`` is already disabled!')
            cursor.execute(f"UPDATE logs SET messageDelete = 0 WHERE guild_id = {ctx.guild.id}")
            await ctx.send("Logging ``message deletion`` is now disabled.")
            db.commit()
            cursor.close()
            db.close()
        elif setting.lower() == "member leave" or setting.lower() == "members leaving":
            if settings[6] == 0:
                return await ctx.send(f'Logging ``members leaving`` is already disabled!')
            cursor.execute(f"UPDATE logs SET memberLeave = 0 WHERE guild_id = {ctx.guild.id}")
            await ctx.send("Logging ``members leaving`` is now disabled.")
            db.commit()
            cursor.close()
            db.close()
        elif setting.lower() == "member join" or setting.lower() == "members joining":
            if settings[7] == 0:
                return await ctx.send(f'Logging ``members joining`` is already disabled!')
            cursor.execute(f"UPDATE logs SET memberJoin = 0 WHERE guild_id = {ctx.guild.id}")
            await ctx.send("Logging ``members joining`` is now disabled.")
            db.commit()
            cursor.close()
            db.close()
        elif setting.lower() == "channel deleted" or setting.lower() == "channel delete" or setting.lower() == "channel deletion":
            if settings[8] == 0:
                return await ctx.send(f'Logging ``channel deletion`` is already disabled!')
            cursor.execute(f"UPDATE logs SET channelDelete = 0 WHERE guild_id = {ctx.guild.id}")
            await ctx.send("Logging ``channel deletion`` is now disabled.")
            db.commit()
            cursor.close()
            db.close()
        elif setting.lower() == "channel created" or setting.lower() == "channel create" or setting.lower() == "channel creation":
            if settings[9] == 0:
                return await ctx.send(f'Logging ``channel creation`` is already disabled!')
            cursor.execute(f"UPDATE logs SET channelCreate = 0 WHERE guild_id = {ctx.guild.id}")
            await ctx.send("Logging ``channel creation`` is now disabled.")
            db.commit()
            cursor.close()
            db.close()
        elif setting.lower() == "bulk message delete" or setting.lower() == "bulk message deletion":
            if settings[10] == 0:
                return await ctx.send(f'Logging ``bulk message deletion`` is already disabled!')
            cursor.execute(f"UPDATE logs SET bulkMessageDelete = 0 WHERE guild_id = {ctx.guild.id}")
            await ctx.send("Logging ``bulk message deletion`` is now disabled.")
            db.commit()
            cursor.close()
            db.close()
        else:
            await ctx.send(f"{ctx.author.mention}, that isn't a valid setting!")

    @logs.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def enable(self, ctx, *, setting):
        """
        Enable logging a specified action.
        """
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT roleCreated, roleDeleted, memberBanned, memberMuted, messageEdit, messageDelete, memberLeave, memberJoin, channelDelete, channelCreate, bulkMessageDelete FROM logs WHERE guild_id = {ctx.guild.id}")
        settings = cursor.fetchone()
        if setting.lower() == "role created" or setting.lower() == "role creation":
            if settings[0] == 1:
                return await ctx.send(f'Logging ``role creation`` is already enabled!')
            cursor.execute(f"UPDATE logs SET roleCreated = 1 WHERE guild_id = {ctx.guild.id}")
            await ctx.send("Logging ``role creation`` is now enabled.")
            db.commit()
            cursor.close()
            db.close()
        elif setting.lower() == "role deleted" or setting.lower() == "role deletion":
            if settings[1] == 1:
                return await ctx.send(f'Logging ``role deletion`` is already enabled!')
            cursor.execute(f"UPDATE logs SET roleDeleted = 1 WHERE guild_id = {ctx.guild.id}")
            await ctx.send("Logging ``role deletion`` is now enabled.")
            db.commit()
            cursor.close()
            db.close()
        elif setting.lower() == "member banned" or setting.lower() == "member banning" or setting.lower() == "member unbanning" or setting.lower() == "member banning/unbanning":
            if settings[2] == 1:
                return await ctx.send(f'Logging ``member banning/unbanning`` is already enabled!')
            cursor.execute(f"UPDATE logs SET memberBanned = 1 WHERE guild_id = {ctx.guild.id}")
            await ctx.send("Logging member ``banning/unbanning`` is now enabled.")
            db.commit()
            cursor.close()
            db.close()
        elif setting.lower() == "member muted" or setting.lower() == "member muting" or setting.lower() == "member unmuting" or setting.lower() == "member muting/unmuting":
            if settings[3] == 1:
                return await ctx.send(f'Logging member ``muting/unmuting`` is already enabled!')
            cursor.execute(f"UPDATE logs SET memberMuted = 1 WHERE guild_id = {ctx.guild.id}")
            await ctx.send("Logging member ``muting/unmuting`` is now enabled.")
            db.commit()
            cursor.close()
            db.close()
        elif setting.lower() == "message edited" or setting.lower() == "message edits":
            if settings[4] == 1:
                return await ctx.send(f'Logging ``message edits`` is already enabled!')
            cursor.execute(f"UPDATE logs SET messageEdit = 1 WHERE guild_id = {ctx.guild.id}")
            await ctx.send("Logging ``message edits`` is now enabled.")
            db.commit()
            cursor.close()
            db.close()
        elif setting.lower() == "message deleted" or setting.lower() == "message deletion":
            if settings[5] == 1:
                return await ctx.send(f'Logging ``message deletion`` is already enabled!')
            cursor.execute(f"UPDATE logs SET messageDelete = 1 WHERE guild_id = {ctx.guild.id}")
            await ctx.send("Logging ``message deletion`` is now enabled.")
            db.commit()
            cursor.close()
            db.close()
        elif setting.lower() == "member leave" or setting.lower() == "members leaving":
            if settings[6] == 1:
                return await ctx.send(f'Logging ``members leaving`` is already enabled!')
            cursor.execute(f"UPDATE logs SET memberLeave = 1 WHERE guild_id = {ctx.guild.id}")
            await ctx.send("Logging ``members leaving`` is now enabled.")
            db.commit()
            cursor.close()
            db.close()
        elif setting.lower() == "member join" or setting.lower() == "members joining":
            if settings[7] == 1:
                return await ctx.send(f'Logging ``members joining`` is already enabled!')
            cursor.execute(f"UPDATE logs SET memberJoin = 1 WHERE guild_id = {ctx.guild.id}")
            await ctx.send("Logging ``members joining`` is now enabled.")
            db.commit()
            cursor.close()
            db.close()
        elif setting.lower() == "channel deleted" or setting.lower() == "channel delete" or setting.lower() == "channel deletion":
            if settings[8] == 1:
                return await ctx.send(f'Logging ``channel deletion`` is already enabled!')
            cursor.execute(f"UPDATE logs SET channelDelete = 1 WHERE guild_id = {ctx.guild.id}")
            await ctx.send("Logging ``channel deletion`` is now enabled.")
            db.commit()
            cursor.close()
            db.close()
        elif setting.lower() == "channel created" or setting.lower() == "channel create" or setting.lower() == "channel creation":
            if settings[9] == 1:
                return await ctx.send(f'Logging ``channel creation`` is already enabled!')
            cursor.execute(f"UPDATE logs SET channelCreate = 1 WHERE guild_id = {ctx.guild.id}")
            await ctx.send("Logging ``channel creation`` is now enabled.")
            db.commit()
            cursor.close()
            db.close()
        elif setting.lower() == "bulk message delete" or setting.lower() == "bulk message deletion":
            if settings[10] == 1:
                return await ctx.send(f'Logging ``bulk message deletion`` is already enabled!')
            cursor.execute(f"UPDATE logs SET bulkMessageDelete = 1 WHERE guild_id = {ctx.guild.id}")
            await ctx.send("Logging ``bulk message deletion`` is now enabled.")
            db.commit()
            cursor.close()
            db.close()
        else:
            await ctx.send(f"{ctx.author.mention}, that isn't a valid setting!")


    @logs.command(aliases=['sc', 'set', 'channel', 'setup'])
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def setchannel(self, ctx, channel : discord.TextChannel=None):
        """
        Set the channel for logs to be stored.
        """
        if channel == None:
            return await ctx.send('You need to specify a channel!')
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT channel_id FROM logs WHERE guild_id = '{ctx.guild.id}'") 
        result = cursor.fetchone()
        if result is None:
            sql = ("INSERT INTO logs(guild_id, channel_id, roleCreated, roleDeleted, memberBanned, memberMuted, messageEdit, messageDelete, memberLeave, memberJoin, channelDelete, channelCreate, bulkMessageDelete) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)")
            val = (ctx.guild.id, channel.id, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
            cursor.execute(sql, val)
            db.commit()
        elif result[0] == channel.id:
            return await ctx.send("Logs are already being written in this channel!")
        cursor.execute(f"UPDATE logs SET channel_id = '{channel.id}' WHERE guild_id = '{ctx.guild.id}'")
        db.commit()
        cursor.close()
        db.close()
        await ctx.send(f"Logs are now being recorded in {channel.mention}")

    @logs.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def settings(self, ctx):
        """
        Display the current logging settings.
        """
        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()
        emoji = ['🟥', '🟩']
        cursor.execute(f"SELECT roleCreated, roleDeleted, memberBanned, memberMuted, messageEdit, messageDelete, memberLeave, memberJoin, channelDelete, channelCreate, bulkMessageDelete FROM logs WHERE guild_id = '{ctx.guild.id}'")
        result = cursor.fetchone()
        if result is None:
            return await ctx.send("Please set up logs first.")
        roleCreated = result[0]
        roleDeleted = result[1]
        memberBanned = result[2]
        memberMuted = result[3]
        messageEdit = result[4]
        messageDelete = result[5]
        memberLeave = result[6]
        memberJoin = result[7]
        channelDelete = result[8]
        channelCreate = result[9]
        bulkMessageDelete = result[10]
        emojis = [emoji[roleCreated], emoji[roleDeleted], emoji[memberBanned], emoji[memberMuted], emoji[messageEdit], emoji[messageDelete], emoji[memberLeave], emoji[memberJoin], emoji[channelDelete], emoji[channelCreate], emoji[bulkMessageDelete]]
        embed = discord.Embed()
        embed.set_author(name=f"Logging settings for {ctx.guild.name}", icon_url=ctx.guild.icon_url)
        embed.add_field(name=f"Log Role Creation: {emojis[0]}", value="\u200b", inline=False)
        embed.add_field(name=f"Log Role Deletion: {emojis[1]}", value="\u200b", inline=False)
        embed.add_field(name=f"Log Member Banned: {emojis[2]}", value="\u200b", inline=False)
        embed.add_field(name=f"Log Member Muted: {emojis[3]}", value="\u200b", inline=False)
        embed.add_field(name=f"Log Message Edited: {emojis[4]}", value="\u200b", inline=False)
        embed.add_field(name=f"Log Message Deleted: {emojis[5]}", value="\u200b", inline=False)
        embed.add_field(name=f"Log Member Leave: {emojis[6]}", value="\u200b", inline=False)
        embed.add_field(name=f"Log Member Join: {emojis[7]}", value="\u200b", inline=False)
        embed.add_field(name=f"Log Channel Deleted: {emojis[8]}", value="\u200b", inline=False)
        embed.add_field(name=f"Log Channel Created: {emojis[9]}", value="\u200b", inline=False)
        embed.add_field(name=f"Log Bulk Message Delete: {emojis[10]}", value="\u200b", inline=False)
        await ctx.send(embed=embed)
        cursor.close()
        db.close()

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
        cursor.execute(f"SELECT channel_id, messageDelete FROM logs WHERE guild_id = {payload.guild_id}")
        result = cursor.fetchone()
        if result == None or result[1] == 0:
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
        cursor.execute(f"SELECT channel_id, messageEdit FROM logs WHERE guild_id = {before.guild.id}")
        result = cursor.fetchone()
        if result == None or result[1] == 0:
            return
        channelid = result[0]
        channel = self.bot.get_channel(int(channelid))
        await channel.send(f"`[({current_time})]` - **Message Edited**\n```User: {before.author} (ID: {before.author.id})\nBefore: {before.content}\nAfter: {after.content}``` ``Channel:`` {before.channel.mention}")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT channel_id, memberLeave FROM logs WHERE guild_id = {member.guild.id}")
        result = cursor.fetchone()
        if result == None or result[1] == 0:
            return
        channelid = result[0]
        channel = self.bot.get_channel(int(channelid))
        await channel.send(f"`[({current_time})]` - **User Left Guild**\n```User: {member} (ID: {member.id})```")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT channel_id, memberJoin FROM logs WHERE guild_id = {member.guild.id}")
        result = cursor.fetchone()
        if result == None or result[1] == 0:
            return
        channelid = result[0]
        channel = self.bot.get_channel(int(channelid))
        await channel.send(f"`[({current_time})]` - **User Joined Guild**\n```User: {member} (ID: {member.id})```")

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        guild_id = role.guild.id
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT channel_id, roleCreated FROM logs WHERE guild_id = {guild_id}")
        result = cursor.fetchone()
        if result == None or result[1] == 0:
            return
        channelid = result[0]
        channel = self.bot.get_channel(int(channelid))
        await channel.send(f"`[({current_time})]` - **Role Created**\n```Name: {role.name} (ID: {role.id})`\nHoist?: {role.hoist}\nPosition: {role.position}\nMentionable: {role.mentionable}\nColor: {role.color}```")
    
    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        guild_id = role.guild.id
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT channel_id, roleDeleted FROM logs WHERE guild_id = {guild_id}")
        result = cursor.fetchone()
        if result == None or result[1] == 0:
            return
        channelid = result[0]
        channel = self.bot.get_channel(int(channelid))
        await channel.send(f"`[({current_time})]` - **Role Deleted**\n```Name: {role.name} (ID: {role.id})```")

    @commands.Cog.listener()
    async def on_raw_bulk_message_delete(self, payload):
        guild_id = payload.guild_id
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT channel_id, bulkMessageDelete FROM logs WHERE guild_id = {guild_id}")
        result = cursor.fetchone()
        if result == None or result[1] == 0:
            return
        channelid = result[0]
        channel = self.bot.get_channel(int(channelid))
        channel2 = self.bot.get_channel(payload.channel_id)
        await channel.send(f"`[({current_time})]` - **Bulk Message Deletion**\n```Channel: {channel2.name} (ID: {payload.channel_id})```")

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        guild_id = channel.guild.id
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT channel_id, channelCreate FROM logs WHERE guild_id = {guild_id}")
        result = cursor.fetchone()
        if result == None or result[1] == 0:
            return
        channelid = result[0]
        channel1 = self.bot.get_channel(int(channelid))
        if channel.Connectable:
            t = "Voice"
        else:
            t = "Text"
        await channel1.send(f"`[({current_time})]` - **Channel Created [{channel.mention}]**\n```Channel: {channel.name} (ID: {channel.id})\nType: {t}\nPosition: {channel.position}\nCategory: {channel.category}```")
    
    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        guild_id = channel.guild.id
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT channel_id, channelCreate FROM logs WHERE guild_id = {guild_id}")
        result = cursor.fetchone()
        if result == None or result[1] == 0:
            return
        channelid = result[0]
        channel1 = self.bot.get_channel(int(channelid))
        try:
            if channel.Connectable:
                t = "Voice"
        except:
            t = "Text"
        await channel1.send(f"`[({current_time})]` - **Channel Deleted**\n```Channel: {channel.name} (ID: {channel.id})\nType: {t}\nPosition: {channel.position}\nCategory: {channel.category}```")
        

def setup(client):
    client.add_cog(Logs(client))
    now = datetime.now()
    print(f'{now} | Loaded logging module.')