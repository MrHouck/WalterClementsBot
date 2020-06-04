import discord
from discord.ext import commands
from discord.ext import menus
from datetime import datetime
import itertools
import json
import os
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))


commandcount = 0
totalPages = 0

def constructPage(index):
    with open(THIS_FOLDER + '/resources/pages.json', 'r') as f:
        pages = json.load(f)
        f.close()

    embed = discord.Embed(color=0x7289da, title=f"**Commands**")
    embed.set_author(name=f'Page {index+1}/{len(pages)} ({commandcount} commands)')
    for command in pages[str(index)]:
        if "aliases" in pages[str(index)][command]:
            cmd = f'+[{pages[str(index)][command]["name"]}'
            for alias in pages[str(index)][command]["aliases"]:
                cmd += f'|{alias}'
            cmd += ']'
        else:
            cmd = f'+{pages[str(index)][command]["name"]}'
        cmdHelp = pages[str(index)][command]["help"]
        if pages[str(index)][command]["usage"] == "":
            cmdHelp += f'\n`Usage: +{command}`'
        else:
            cmdHelp += f'\n`Usage: +{command} {pages[str(index)][command]["usage"]}`'
        embed.add_field(name=cmd, value=cmdHelp, inline=False)
    embed.set_footer(text="Still need help? Join https://discord.gg/GdWwJpS")
    return embed

class HelpMenu(menus.Menu):
    pageIndex = 0

    async def send_initial_message(self, ctx, channel):        
        return await channel.send(embed=constructPage(self.pageIndex))

    @menus.button('\N{BLACK LEFT-POINTING DOUBLE TRIANGLE WITH VERTICAL BAR}')
    async def on_to_start_button(self, payload):
        self.pageIndex = 0
        await self.message.edit(embed=constructPage(self.pageIndex))


    @menus.button('\N{BLACK LEFT-POINTING TRIANGLE}')
    async def on_back_one_button(self, payload):
        self.pageIndex = self.pageIndex - 1
        if self.pageIndex < 0:
            self.pageIndex = totalPages-1
        await self.message.edit(embed=constructPage(self.pageIndex))

    @menus.button('\N{BLACK SQUARE FOR STOP}')
    async def on_stop_button(self, payload):
        self.pageIndex = 0
        await self.message.delete()
    @menus.button('\N{BLACK RIGHT-POINTING TRIANGLE}')
    async def on_forward_one_button(self, payload):
        self.pageIndex = self.pageIndex + 1
        if self.pageIndex > totalPages-1:
            self.pageIndex = 0
        await self.message.edit(embed=constructPage(self.pageIndex))


    @menus.button('\N{BLACK RIGHT-POINTING DOUBLE TRIANGLE WITH VERTICAL BAR}')
    async def on_to_end_button(self, payload):
        self.pageIndex = totalPages-1
        await self.message.edit(embed=constructPage(self.pageIndex))

class Help(commands.Cog):
    def __init__(self, client):
        self.bot = client

    def createJSON(self, commands):
        pages = {}   
        i = 0
        j = 0
        sortedCommands = []
        for command in commands:
            sortedCommands.append(command.name)
        
        sortedCommands.sort()        
        for command in sortedCommands:
            command = self.bot.get_command(command)
            if not command.hidden:
                if j == 0:
                    pages[str(i)] = {}
                pages[str(i)][command.name] = {}
                pages[str(i)][command.name]["name"] = {}
                pages[str(i)][command.name]["help"] = {}
                pages[str(i)][command.name]["usage"] = {}
                pages[str(i)][command.name]["name"] = command.name
                try:
                    commandHelp = command.help
                except:
                    commandHelp = ""
                pages[str(i)][command.name]["help"] = command.help
                usage = "" if not command.usage else command.usage
                pages[str(i)][command.name]["usage"] = usage
                if len(command.aliases) >= 1:
                    pages[str(i)][command.name]["aliases"] = []
                    pages[str(i)][command.name]["aliases"] = command.aliases
                j += 1
                if j >= 10:
                    i += 1
                    j = 0
            else:
                pass
        global totalPages
        totalPages = len(pages)
        with open(THIS_FOLDER + '/resources/pages.json', 'w') as f:
            json.dump(pages, f, indent=4)

    @commands.command()
    async def help(self, ctx):
        """
        hmmm......
        """
        self.createJSON(self.bot.commands)
        global commandcount 
        commandcount = len(self.bot.commands)
        menu = HelpMenu()
        await menu.start(ctx)

def setup(client):
    client.add_cog(Help(client))
    now = datetime.now()
    print(f"{now} | Loaded help module.")
