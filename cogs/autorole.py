import discord
import asyncio
from datetime import datetime, timedelta
from discord.ext import commands
from discord.utils import get
import random #for random embed colors
import sqlite3


class Autorole(commands.Cog):
    def __init__(self, client):
        self.bot = client

    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    async def autorole(self, ctx):
        """
        Base command for autorole.
        """
        if ctx.invoked_subcommand == None:
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()
            guild = ctx.guild
            cursor.execute(f"SELECT enabled, roles FROM autorole WHERE guild_id = '{guild.id}'")
            result = cursor.fetchone()
            if result is None or result[1] is None:
                embed = discord.Embed(title="**Autorole**", color=random.randint(1, 0xffffff), inline=False)
                embed.add_field(name='Autorole is currently **__disabled__**', value="To get started, use one of the subcommands. (enable, disable, add, remove, clear)", inline=False)
                return await ctx.send(embed=embed)
            else:
                roleIds = result[1].split('|')
                roleObjs = []
                for roleId in roleIds:
                    roleObjs.append(ctx.guild.get_role(int(roleId)))
                isEnabled = result[0] 
                isEnabled = "enabled" if result[0].lower() == "true" else "disabled"
                embed = discord.Embed(title="**Autorole**", color=roleObjs[0].color)
                embed.add_field(name=f'Autorole is currently **__{isEnabled}__**', value="\u200b", inline=False)
                embed.add_field(name='Auto-assigned roles:', value=" ".join([role.mention + '\n' for role in roleObjs]), inline=False)
                embed.add_field(name='Subcommands', value='enable\ndisable\nadd\nremove\nclear')
                return await ctx.send(embed=embed)

    @autorole.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def add(self, ctx, *, role: discord.Role):
        """
        Add a role that will be automatically assigned when a user joins.
        """
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        guild = ctx.guild
        cursor.execute(f"SELECT enabled, roles FROM autorole WHERE guild_id = '{guild.id}'")
        result = cursor.fetchone()
        #if the thing from db is none
        if result is None:
            sql = ("INSERT INTO autorole(guild_id, roles, enabled) VALUES(?,?,?)")
            val = (guild.id, role.id, "true")
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()
            return await ctx.send(f"Added {role.name} to auto-assigned roles.")

        if not result[1]:
            cursor.execute(f"UPDATE autorole SET roles = '{role.id}', enabled='true' WHERE guild_id = '{guild.id}'")
        elif str(role.id) in result[1]:       
            return await ctx.send(f"{role.name} is already being automatically assigned!")
        else:
            cursor.execute(f"UPDATE autorole SET roles = '{result[1]+'|'+str(role.id)}' WHERE guild_id = '{guild.id}'")
        db.commit()
        cursor.close()
        db.close()
        return await ctx.send(f"Added {role.name} to auto-assigned roles.")

    @autorole.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def remove(self, ctx, *, role: discord.Role):
        """
        Remove a role from a list of automatically assigned roles.
        """
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        guild = ctx.guild
        cursor.execute(f"SELECT enabled, roles FROM autorole WHERE guild_id = '{guild.id}'")
        result = cursor.fetchone()
        #if there are no db entries /
        #if there are no roles /
        #if the role doesn't exist /
        #if the role isn't in list of auto-assigned /
        if result is None:
            return await ctx.send("Autoroles have not been setup yet!")
        elif result[1] is None:
            return await ctx.send("There are no roles being auto-assigned!")
        elif str(role.id) not in result[1]:
            return await ctx.send(f"{role} isn't being auto-assigned!")
        #remove from DB
        
        updatedList = result[1].split('|')
        updatedList.pop(updatedList.index(str(role.id)))
        updatedQuery = ""
        for _id in updatedList:
            updatedQuery += _id + '|'
        updatedQuery = updatedQuery[:-1]
        if not updatedList:
            cursor.execute(f"UPDATE autorole SET roles=NULL, enabled='false' WHERE guild_id = '{guild.id}'")
        else:
            cursor.execute(f"UPDATE autorole SET roles='{updatedQuery}' WHERE guild_id = '{guild.id}'")
        db.commit()
        cursor.close()
        db.close()
        return await ctx.send(f"Removed {role.name} from auto-assigned roles.")


        


    @autorole.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx):
        """
        Clear the list of roles being auto-assigned
        """
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        guild = ctx.guild
        cursor.execute(f"SELECT enabled, roles FROM autorole WHERE guild_id = '{guild.id}'")
        result = cursor.fetchone()
        if result[1] is None:
            return await ctx.send("There are no roles being auto-assigned!")
        else:
            cursor.execute(f"UPDATE autorole SET enabled='false', roles=NULL WHERE guild_id = '{guild.id}'")
        db.commit()
        cursor.close()
        db.close()
        return await ctx.send("Success! Auto-assigned roles have been cleared.")



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
            return await ctx.send("Autoroles have not been setup yet!")
        elif result == "false":
            return await ctx.send("Auto-assigning roles is already disabled!")
        else:
            cursor.execute(f"UPDATE autorole SET enabled = 'false' WHERE guild_id = '{guild.id}'")
            db.commit()
            cursor.close()
            db.close()
            return await ctx.message.add_reaction('\U00002705')
    
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
        cursor.execute(f"SELECT roles, enabled FROM autorole WHERE guild_id = '{guild.id}'")
        result = cursor.fetchone()
        if result is None or result[0] is None:
            return await ctx.send("Autoroles have not been setup yet!")
        elif result[1] == "true":
            return await ctx.send("Auto-assigning roles is already enabled!")
        else:
            cursor.execute(f"UPDATE autorole SET enabled = 'true' WHERE guild_id = '{guild.id}'")
            db.commit()
            cursor.close()
            db.close()
            return await ctx.message.add_reaction('\U00002705')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT roles, enabled FROM autorole WHERE guild_id = '{member.guild.id}'")
        result = cursor.fetchone()
        if result is None:
            return 
        if result[1] == 'false':
            return
        if result[0] is None:
            return

        roleIds = result[0].split('|')
        roleObjs = [member.guild.get_role(int(roleId)) for roleId in roleIds]
        for obj in roleObjs:
            await member.add_roles(obj)



def setup(client):
    client.add_cog(Autorole(client))
    now = datetime.now()
    print(f'{now} | Loaded autorole module.')