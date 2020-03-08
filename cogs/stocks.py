import discord
import asyncio
import random
from discord.ext import commands
import sqlite3

class Stocks(commands.Cog):
    def __init__(self, client):
        self.bot = client

    @commands.command()
    @commands.is_owner()
    @commands.guild_only()
    async def stockinit(self, ctx):
        while True:
            await ctx.trigger_typing()
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()
            cursor.execute("SELECT walterStock, ypyStock, redditStock, smartphownedStock FROM stocks")
            data = cursor.fetchone()
            walterStock = data[0]
            ypyStock = data[1]
            redditStock = data[2]
            smartphownedStock = data[3]
            decrease = random.uniform(0.001000, 0.004000)
            increase = random.uniform(0.001000, 0.004000)
            whichStock = random.randint(1, 4)
            decrease = round(decrease, 6)
            increase = round(increase, 6)
            if whichStock == 1: #walter stock
                rEmoji = '➖'
                yEmoji = '➖'
                sEmoji = '➖'
                rChange = 0.000
                yChange = 0.000
                sChange = 0.000
                upRedditStock = redditStock
                upSmartphownedStock = smartphownedStock
                upYpyStock = ypyStock
                how = random.randint(1, 3)
                if how == 1:
                    #no change
                    wEmoji = '➖'
                    wChange = 0.000
                    upWalterStock = walterStock
                elif how == 2:
                    #decrease
                    wChange = -1 * (walterStock * decrease)
                    upWalterStock = walterStock + wChange
                    wEmoji = '📉'
                else:
                    #increase
                    wChange = (walterStock * increase)
                    upWalterStock = walterStock + wChange
                    wEmoji = '📈'


            elif whichStock == 2: #ypy stock
                rEmoji = '➖'
                wEmoji = '➖'
                sEmoji = '➖'
                rChange = 0.000
                wChange = 0.000
                sChange = 0.000
                upRedditStock = redditStock
                upSmartphownedStock = smartphownedStock
                upWalterStock = walterStock
                how = random.randint(1, 3)
                if how == 1:
                    #no change
                    yEmoji = '➖'
                    yChange = 0.000
                    upWalterStock = ypyStock
                elif how == 2:
                    #decrease
                    yChange = -1 * (ypyStock * decrease)
                    upYpyStock = ypyStock + yChange
                    yEmoji = '📉'
                else:
                    #increase
                    yChange = ypyStock * increase
                    upYpyStock = ypyStock + yChange
                    yEmoji = '📈'


            elif whichStock == 3: #reddit stock
                yEmoji = '➖'
                wEmoji = '➖'
                sEmoji = '➖'
                yChange = 0.000
                wChange = 0.000
                sChange = 0.000
                upYpyStock = ypyStock
                upSmartphownedStock = smartphownedStock
                upWalterStock = walterStock
                how = random.randint(1, 3)
                if how == 1:
                    #no change in stock
                    rEmoji = '➖'
                    rChange = 0.000
                    upRedditStock = redditStock
                elif how == 2:
                    #decrease
                    rChange = -1 * (redditStock * decrease)
                    upRedditStock = redditStock + rChange
                    rEmoji = '📉'
                else:
                    #increase
                    rChange = (redditStock * increase)
                    upRedditStock = redditStock + rChange
                    rEmoji = '📈'


            elif whichStock == 4: #smartphowned stock
                yEmoji = '➖'
                wEmoji = '➖'
                rEmoji = '➖'
                yChange = 0.000
                wChange = 0.000
                rChange = 0.000
                upYpyStock = ypyStock
                upRedditStock = redditStock
                upWalterStock = walterStock
                how = random.randint(1, 3)
                if how == 1:
                    #no change in stock
                    sEmoji = '➖'
                    sChange = 0.000
                    upSmartphownedStock = smartphownedStock
                elif how == 2:
                    #decrease
                    sChange = -1 * (smartphownedStock * decrease)
                    upSmartphownedStock = smartphownedStock + change
                    sEmoji = '📉'
                else:
                    #increase
                    sChange = (redditStock * increase)
                    upSmartphownedStock = smartphownedStock + change
                    sEmoji = '📈'
            cursor.execute(f"UPDATE stocks SET walterStock = {upWalterStock}")
            cursor.execute(f"UPDATE stocks SET ypyStock = {upYpyStock}")
            cursor.execute(f"UPDATE stocks SET redditStock = {upRedditStock}")
            cursor.execute(f"UPDATE stocks SET smartphownedStock = {upSmartphownedStock}")
            db.commit()
            cursor.close()
            db.close()
            embed = discord.Embed(title='Stock Update!')
            embed.add_field(name='Walter Clements Stock', value=f'{wEmoji} {wChange}    -    {upWalterStock}💠', inline=False)
            embed.add_field(name='Youngpeopleyoutube Stock', value=f'{yEmoji} {yChange}    -    {upYpyStock}💠', inline=False)
            embed.add_field(name='Reddit Stock', value=f'{rEmoji} {rChange}    -    {upRedditStock}💠', inline=False)
            embed.add_field(name='SmartphOWNED Stock', value=f'{sEmoji} {sChange}    -    {upSmartphownedStock}💠', inline=False)
            channel = discord.utils.get(ctx.guild.text_channels, name='stocks')
            await channel.send(embed=embed)
            await asyncio.sleep(600)

    @commands.group()
    @commands.guild_only()
    async def stocks(self, ctx):
        await ctx.trigger_typing()
        if ctx.invoked_subcommand is None:
            await ctx.send('Please use one of the subcommands! (``buy, view, sell``)')

    @stocks.command()
    @commands.guild_only()
    async def view(self, ctx):
        await ctx.trigger_typing()
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute("SELECT walterStock, ypyStock, redditStock, smartphownedStock, walterShares, ypyShares, redditShares, smartShares FROM stocks")
        data = cursor.fetchone()
        walterVal = data[0]
        ypyVal = data[1]
        redditVal = data[2]
        smartphownedVal = data[3]
        walterShares = data[4]
        ypyShares = data[5]
        redditShares = data[6]
        smartphownedShares = data[7]
        embed = discord.Embed(title='Current Stock Market:', color=ctx.author.color)
        embed.add_field(name='Walter Clements Stock', value=f'{walterVal}💠 - {walterShares} shares', inline=False)
        embed.add_field(name='Youngpeopleyoutube Stock', value=f'{ypyVal}💠 - {ypyShares} shares', inline=False)
        embed.add_field(name='Reddit Stock', value=f'{redditVal}💠 - {redditShares} shares', inline=False)
        embed.add_field(name='SmartphOWNED Stock', value=f'{smartphownedVal}💠 - {smartphownedShares} shares', inline=False)
        cursor.close()
        db.close()
        await ctx.send(embed=embed)

    @stocks.command()
    @commands.guild_only()
    async def sell(self, ctx, stock, amount : int=1):
        await ctx.trigger_typing()
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT user_id, money FROM economy WHERE guild_id = {ctx.guild.id} and user_id = {ctx.author.id}")
        result = cursor.fetchone()
        if result is None:
            await ctx.send(f"{ctx.author.mention}, you need to register first!")
            return
        balance = float(result[1])
        possibilities = "ypy walter reddit smartphowned"
        if stock not in possibilities:
            await ctx.send("That is not a valid type of stock! Valid types are: ``ypy, walter, reddit, and smartphowned.``")
            return
        cursor.execute(f"SELECT wshares, yshares, rshares, sshares FROM economy WHERE guild_id = {ctx.guild.id} and user_id = {ctx.author.id}")
        stocks = cursor.fetchone()
        walterShares = stocks[0]
        ypyShares = stocks[1]
        redditShares = stocks[2]
        smartphownedShares = stocks[3]
        cursor.execute(f"SELECT walterShares, ypyShares, redditShares, smartShares FROM stocks")
        stocks = cursor.fetchone()
        cWalterShares = stocks[0]
        cYpyShares = stocks[1]
        cRedditShares = stocks[2]
        cSmartShares = stocks[3]
        if stock == 'walter':
            cursor.execute("SELECT walterStock FROM stocks")
            walterStock = cursor.fetchone()
            if amount > walterShares:
                await ctx.send("You don't have that many shares to sell!")
                return
            value = float((amount * walterStock[0] * 0.98))
            balance += value
            cursor.execute(f"UPDATE economy SET wshares = {walterShares - amount} WHERE guild_id = {ctx.guild.id} and user_id = {ctx.author.id}")
            cursor.execute(f"UPDATE stocks SET walterShares = {cWalterShares + amount}")
            cursor.execute(f"UPDATE stocks SET walterStock = {float(walterStock[0] - (value/75))}")
            cursor.execute(f"UPDATE economy SET money = {balance} WHERE guild_id = {ctx.guild.id} and user_id = {ctx.author.id}")
            db.commit()
            cursor.close()
            db.close()
            await ctx.send(f"You have successfully sold {amount} shares in the {stock} industry for {value}💠!")
        if stock == 'ypy':
            cursor.execute("SELECT ypyStock FROM stocks")
            ypyStock = cursor.fetchone()
            if amount > ypyShares:
                await ctx.send("You don't have that many shares to sell!")
                return
            value = float((amount * ypyStock[0] * 0.98))
            balance += value
            cursor.execute(f"UPDATE economy SET yshares = {ypyShares - amount} WHERE guild_id = {ctx.guild.id} and user_id = {ctx.author.id}")
            cursor.execute(f"UPDATE stocks SET ypyShares = {cYpyShares + amount}")
            cursor.execute(f"UPDATE stocks SET ypyStock = {float(ypyStock[0] - (value/75))}")
            cursor.execute(f"UPDATE economy SET money = {balance} WHERE guild_id = {ctx.guild.id} and user_id = {ctx.author.id}")
            db.commit()
            cursor.close()
            db.close()
            await ctx.send(f"You have successfully sold {amount} shares in the {stock} industry for {value}💠!")
        if stock == 'reddit':
            cursor.execute("SELECT redditStock FROM stocks")
            redditStock = cursor.fetchone()
            if amount > redditShares:
                await ctx.send("You don't have that many shares to sell!")
                return
            value = float((amount * redditStock[0] * 0.98))
            balance += value
            cursor.execute(f"UPDATE economy SET rshares = {redditShares - amount} WHERE guild_id = {ctx.guild.id} and user_id = {ctx.author.id}")
            cursor.execute(f"UPDATE stocks SET redditShares = {cRedditShares + amount}")
            cursor.execute(f"UPDATE stocks SET redditStock = {float(redditStock[0] - (value/75))}")
            cursor.execute(f"UPDATE economy SET money = {balance} WHERE guild_id = {ctx.guild.id} and user_id = {ctx.author.id}")
            db.commit()
            cursor.close()
            db.close()
            await ctx.send(f"You have successfully sold {amount} shares in the {stock} industry for {value}💠!")
        if stock == 'smartphowned':
            cursor.execute("SELECT smartphownedStock FROM stocks")
            smartphownedStock = cursor.fetchone()
            if amount > smartphownedShares:
                await ctx.send("You don't have that many shares to sell!")
                return
            value = float((amount * ypyStock[0] * 0.98))
            balance += value
            cursor.execute(f"UPDATE economy SET sshares = {smartphownedShares - amount} WHERE guild_id = {ctx.guild.id} and user_id = {ctx.author.id}")
            cursor.execute(f"UPDATE stocks SET smartShares = {cSmartShares + amount}")
            cursor.execute(f"UPDATE stocks SET smartphownedStock = {float(smartphownedStock[0] - (value/75))}")
            cursor.execute(f"UPDATE economy SET money = {balance} WHERE guild_id = {ctx.guild.id} and user_id = {ctx.author.id}")
            db.commit()
            cursor.close()
            db.close()
            await ctx.send(f"You have successfully sold {amount} shares in the {stock} industry for {value}💠!")

    @stocks.command()
    @commands.guild_only()
    async def buy(self, ctx, stock, amount : int):
        await ctx.trigger_typing()
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT user_id, money FROM economy WHERE guild_id = {ctx.guild.id} and user_id = {ctx.author.id}")
        result = cursor.fetchone()
        if result is None:
            await ctx.send(f"{ctx.author.mention}, you need to register first!")
            return
        balance = float(result[1])
        possibilities = "ypy walter reddit smartphowned"
        if stock not in possibilities:
            await ctx.send("That is not a valid type of stock! Valid types are: ``ypy, walter, reddit, and smartphowned.``")
            return
        if amount == None:
            await ctx.send("Please specify an amount of stock to buy! (Limit of 25)")
        if stock == 'ypy':
            cursor.execute(f"SELECT ypyStock, ypyShares FROM stocks")
            ypy = cursor.fetchone()
            if ypy[1] == 0:
                await ctx.send("There are no more shares of this stock!")
                return
            if (ypy[1] - float(amount)) < 0:
                amount = ypy[1]
            if balance < float((amount * ypy[0] * 1.02)):
                await ctx.send(f"You need {(amount*ypy[0]*1.02) - balance} more 💠 to buy this much stock.")
            else:
                balance -= amount * ypy[0] * 1.02
                cursor.execute(f"UPDATE economy SET money = {balance} WHERE guild_id = {ctx.guild.id} and user_id = {ctx.author.id}")
                stockUpdate = (amount * ypy[0] * 1.02) - amount * ypy[0]
                cursor.execute(f"UPDATE stocks SET ypyShares = {ypy[1] - amount}")
                cursor.execute(f"UPDATE stocks SET ypyStock = {ypy[0] + stockUpdate}")
                cursor.execute(f"SELECT yshares FROM economy WHERE guild_id = {ctx.guild.id} and user_id = {ctx.author.id}")
                cshares = cursor.fetchone()
                cursor.execute(f"UPDATE economy SET yshares = {cshares[0] + amount} WHERE guild_id = {ctx.guild.id} and user_id = {ctx.author.id}")
                db.commit()
                cursor.close()
                db.close()
                await ctx.send(f"You have successfully purchased {amount} stock in the {stock} industry for {amount*ypy[0]*1.02}💠!")
        elif stock == 'walter':
            cursor.execute("SELECT walterStock, walterShares FROM stocks")
            walter = cursor.fetchone()
            if walter[1] == 0:
                await ctx.send("There are no more shares of this stock!")
                return
            if (walter[1] - float(amount)) < 0:
                amount = walter[1]
            if balance < float((amount * walter[0] * 1.02)):
                await ctx.send(f"You need {(amount*walter[0]*1.02) - balance} more 💠 to buy this much stock.")
            else:
                balance -= amount * walter[0] * 1.02
                cursor.execute(f"UPDATE economy SET money = {balance} WHERE guild_id = {ctx.guild.id} and user_id = {ctx.author.id}")
                stockUpdate = (amount * walter[0] * 1.02) - amount * walter[0]
                cursor.execute(f"UPDATE stocks SET walterShares = {walter[1] - amount}")
                cursor.execute(f"UPDATE stocks SET walterStock = {walter[0] + stockUpdate}")
                cursor.execute(f"SELECT wshares FROM economy WHERE guild_id = {ctx.guild.id} and user_id = {ctx.author.id}")
                cshares = cursor.fetchone()
                cursor.execute(f"UPDATE economy SET wshares = {cshares[0] + amount} WHERE guild_id = {ctx.guild.id} and user_id = {ctx.author.id}")
                db.commit()
                cursor.close()
                db.close()
                await ctx.send(f"You have successfully purchased {amount} stock in the {stock} industry for {(amount*walter[0]*1.02)}💠!")
        elif stock == 'reddit':
            cursor.execute("SELECT redditStock, redditShares FROM stocks")
            reddit = cursor.fetchone()
            if reddit[1] == 0:
                await ctx.send("There are no more shares of this stock!")
                return
            if (reddit[1] - float(amount)) < 0:
                amount = reddit[1]
            if balance < float((amount * reddit[0] * 1.02)):
                await ctx.send(f"You need {(amount*reddit[0]*1.02) - balance} more 💠 to buy this much stock.")
            else:
                balance -= amount * reddit[0] * 1.02
                cursor.execute(f"UPDATE economy SET money = {balance} WHERE guild_id = {ctx.guild.id} and user_id = {ctx.author.id}")
                stockUpdate = (amount * reddit[0] * 1.02) - amount * reddit[0]
                cursor.execute(f"UPDATE stocks SET redditShares = {reddit[1] - amount}")
                cursor.execute(f"UPDATE stocks SET redditStock = {reddit[0] + stockUpdate}")
                cursor.execute(f"SELECT rshares FROM economy WHERE guild_id = {ctx.guild.id} and user_id = {ctx.author.id}")
                cshares = cursor.fetchone()
                cursor.execute(f"UPDATE economy SET rshares = {cshares[0] + amount} WHERE guild_id = {ctx.guild.id} and user_id = {ctx.author.id}")
                db.commit()
                cursor.close()
                db.close()
                await ctx.send(f"You have successfully purchased {amount} stock in the {stock} industry for {amount*reddit[0]*1.02}💠!")
        elif stock == 'smartphowned':
            cursor.execute("SELECT smartphownedStock, smartShares FROM stocks")
            smartphowned = cursor.fetchone()
            if smartphowned[1] == 0:
                await ctx.send("There are no more shares of this stock!")
                return
            if (smartphowned[1] - float(amount)) < 0:
                amount = smartphowned[1]
            if balance < float((amount * smartphowned[0] * 1.02)):
                await ctx.send(f"You need {(amount*smartphowned[0]*1.02) - balance} more 💠 to buy this much stock.")
            else:
                balance -= amount * smartphowned[0] * 1.02
                cursor.execute(f"UPDATE economy SET money = {balance} WHERE guild_id = {ctx.guild.id} and user_id = {ctx.author.id}")
                stockUpdate = (amount * walter[0] * 1.02) - amount * smartphowned[0]
                cursor.execute(f"UPDATE stocks SET walterShares = {smartphowned[1] - amount}")
                cursor.execute(f"UPDATE stocks SET walterStock = {smartphowned[0] + stockUpdate}")
                cursor.execute(f"SELECT sshares FROM economy WHERE guild_id = {ctx.guild.id} and user_id = {ctx.author.id}")
                cshares = cursor.fetchone()
                cursor.execute(f"UPDATE economy SET sshares = {cshares[0] + amount} WHERE guild_id = {ctx.guild.id} and user_id = {ctx.author.id}")
                db.commit()
                cursor.close()
                db.close()
                await ctx.send(f"You have successfully purchased {amount} stock in the {stock} industry for {amount*smartphowned[0]*1.02}💠!")

def setup(client):
    client.add_cog(Stocks(client))
    print('Loaded stocks module.')
