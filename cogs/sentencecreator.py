import discord
from discord.ext import commands, tasks
from datetime import datetime
import os


class SentenceCreator(commands.Cog):
    def __init__(self, client):
        self.bot = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == 685974007878647834:
            content = message.content
            if content == "+cleartxt":
                content = ''
                f = open('paragraph.txt', 'w')
                f.write(content)
                f.close()
                return await self.bot.process_commands(message)
            with open('paragraph.txt', 'r') as f:
                paragraph = f.read()
                f.close()
            with open('paragraph.txt', 'w') as f:
                new = paragraph + ' ' + content
                f.write(new)
                f.close()
            ######ZIAD HOSTS THE TEXT FILE AT https://ziad87.me/paragraph.txt ######
            #####backup is at https://ziad87.me/paragraph2.txt#########

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def cleartxt(self, ctx):
        if ctx.guild.id == 530038467032252426:
            with open('paragraph.txt', 'w') as f:
                f.write('')
                f.close()


def setup(client):
    client.add_cog(SentenceCreator(client))
    now = datetime.now()
    print(f'{now} | Loaded sentence creator module.')
