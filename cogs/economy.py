import discord
import json
import os
import asyncio
import random
import datetime
import sqlite3
import numpy
from datetime import datetime, timedelta
from random import choices
from discord.ext import commands
from discord.ext import menus

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
economyInfo = {
            " 🍎":{"price":2500,"multiplier":2},
            " 🌽":{"price":5000,"multiplier":2},
            " ⌚":{"price":10000,"multiplier":2},
            " 🍚":{"price":15000,"multiplier":2},
            " 📙":{"price":20000,"multiplier":2},
            " 🍒":{"price":25000,"multiplier":2},
            " 💙":{"price":30000,"multiplier":2},
            " 🛹":{"price":35000,"multiplier":2},
            " 🔋":{"price":40000,"multiplier":2},
            " ⌛":{"price":50000,"multiplier":3},
            " 🏅":{"price":125000,"multiplier":3},
            " 🐠":{"price":250000,"multiplier":3},
            " 🦞":{"price":500000,"multiplier":3},
            " 💵":{"price":600000,"multiplier":3},
            " 💸":{"price":750000,"multiplier":3},
            " 💰":{"price":1000000,"multiplier":4},
            " 💳":{"price":2500000,"multiplier":4},
            " 📈":{"price":5000000,"multiplier":4},
            " 💎":{"price":10000000,"multiplier":4},
            " 😳":{"price":25000000,"multiplier":4},
            " 😃":{"price":50000000,"multiplier":4},
            " ⭐":{"price":100000000,"multiplier":4},
            " 🎉":{"price":250000000,"multiplier":5},
            " 🤑":{"price":1000000000,"multiplier":10}
        }

class ShopMenu(menus.Menu):
    pageIndex = 0

    def createEmbed(self, index):
        embed = discord.Embed(title=f'**Shop** ({index+1}/3)', color=0x7afbff)
        if index == 0:
            lower = 1
            upper = 9
        else:
            lower = index*10
            upper = index*10+9
        i=1
        for item in economyInfo:
            if lower <= i <= upper: 
                embed.add_field(name="{} - {:,}".format(item, economyInfo[item]['price']), value=f"Gain {economyInfo[item]['multiplier']}x as much money", inline=False)
            i += 1
        embed.set_footer(text="Multipliers stack.")
        return embed

    async def send_initial_message(self, ctx, channel):        
        return await channel.send(embed=self.createEmbed(self.pageIndex))

    @menus.button('\N{BLACK LEFT-POINTING TRIANGLE}')
    async def on_back_one_button(self, payload):
        self.pageIndex = self.pageIndex - 1
        if self.pageIndex < 0:
            self.pageIndex = 2
        await self.message.edit(embed=self.createEmbed(self.pageIndex))

    @menus.button('\N{BLACK SQUARE FOR STOP}')
    async def on_stop_button(self, payload):
        self.pageIndex = 0
        await self.message.delete()

    @menus.button('\N{BLACK RIGHT-POINTING TRIANGLE}')
    async def on_forward_one_button(self, payload):
        self.pageIndex = self.pageIndex + 1
        if self.pageIndex > 2:
            self.pageIndex = 0
        await self.message.edit(embed=self.createEmbed(self.pageIndex))




class Economy(commands.Cog):
    def __init__(self, client):
        self.bot = client

    @commands.command(aliases=["eco"])
    @commands.guild_only()
    async def economy(self, ctx):
        """
        A short guide to the economy
        """
        embed = discord.Embed(title="Economy Overview", color=discord.Color.orange())
        embed.add_field(name="How to get started", value="To get started, do ``+register``. From there, you can claim your daily allowance by using ``+daily``", inline=False)
        embed.add_field(name="Ways to make money", value="There are multiple ways to get money. The first method is using ``+fish``. By doing this you catch a fish with a random value within certain ranges, and it's automatically sold.\nThe second method is using ``+slots``. By default you only bet 1 coin, but you can specify any amount you want. The slot rolling is completely random, and you might lose your money, but if you win, you win big.\nThe third method is retrieving your daily allowance everyday.\nThe fourth and final method is using Towers, but you can get more info about that by using ``+towersinfo``", inline=False)
        embed.add_field(name="Items", value="The economy has a unique way of working. You can use ``+buy`` to buy items from the shop (view by using ``+shop``) which gives you a money multiplier. The cash multiplier only applies to fishing and your daily allowance.")
        return await ctx.send(embed=embed)
    @commands.command(aliases=['bal', 'balance'])
    @commands.guild_only()
    async def stats(self, ctx, member : discord.Member=None):
        """
        Get economy statistics of yourself or another user. The user must be registered.
        """
        #basically a compact if member is none member = ctx.author else member=member
        member = ctx.author if not member else member
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        #checking is they are registered
        cursor.execute(f"SELECT user_id FROM economy WHERE user_id = '{member.id}'")
        result = cursor.fetchone()
        if result is None: #they haven't registered
            if member == ctx.author:
                await ctx.send(f"{ctx.author.mention}, you have not registered!")
            else:
                await ctx.send('That user has not registered!')
            cursor.close()
            db.close()
        else:
            #getting the goods
            cursor.execute(f"SELECT money, inventory, nextDaily FROM economy WHERE user_id = '{member.id}'")
            result = cursor.fetchone()
            userBalance = result[0]
            userInventory = result[1]
            nextDaily = result[2]
            userInventory = userInventory.replace(',', ' ')
            if userInventory == " ":
                userInventory = "\u200b"
            nextDaily = datetime.strptime(nextDaily, '%Y-%m-%d %H:%M:%S.%f')
            today=datetime.today()
            trueNextDaily = nextDaily-today
            try:
                trueNextDaily = datetime.strptime(str(trueNextDaily), '%H:%M:%S.%f')
                hours = trueNextDaily.hour
                minutes = trueNextDaily.minute
            except:
                hours=0
                minutes=0
            embed = discord.Embed(color=member.color, timestamp=ctx.message.created_at) #using the members top role color
            embed.set_thumbnail(url=member.avatar_url) #getting the tagged members picture and setting it as the thumbnail
            embed.set_author(name=f'Economy Stats - {member}')
            embed.add_field(name='Balance:', value=f'{round(float(userBalance), 3)} 💠', inline=False) #adding the users balance
            embed.add_field(name='Inventory:', value=f'{userInventory}', inline=False) #adding the Inventory
            embed.add_field(name='Next Daily:', value=f'{hours} hours and {minutes} minutes')
            embed.set_footer(text=f'User ID: {member.id}')
            await ctx.send(embed=embed)
            cursor.close()
            db.close()

    @commands.command()
    @commands.guild_only()
    async def register(self, ctx):
        """
        Add yourself to the economy database.
        """
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        #getting user id from economy to check if they are already registered
        cursor.execute(f"SELECT user_id FROM economy WHERE user_id = '{ctx.author.id}'")
        result = cursor.fetchone()
        if result is None:
            today = datetime.today() #for the nextdaily value
            sql = ("INSERT INTO economy(user_id, money, inventory, nextDaily) VALUES(?, ?, ?, ?)")
            val = (ctx.author.id, 100, " ", str(today)) 
            cursor.execute(sql, val)
            db.commit() 
            sql = ("INSERT INTO towers(user_id, toClaim, coinsPerHour, homes, groceryStores, restaurants, clothingStores, electronicsStores, factories, banks, spaceStations) VALUES(?, ?, ?, ?, ?)")
            val = (ctx.author.id, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0)
            cursor.execute(sql, val)
            db.commit() 
            cursor.close()
            db.close()
            #send embed
            embed = discord.Embed(title='*Registered!*', color=ctx.message.author.color)
            embed.add_field(name='You have been added to the database!', value='To start off, you have been credited __100 coins__.')
            embed.set_footer(text="Also, because of the idle money maker, you make 10 coins per hour!")
            await ctx.send(embed=embed)
            return
        else:
            await ctx.send(f'You\'ve already registered, {ctx.author.mention}!')
            cursor.close()
            db.close()
            return
    
    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def fish(self, ctx):
        """
        Fish for different rarities of fish. (Must be registered)
        """
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT user_id FROM economy WHERE user_id = '{ctx.author.id}'")
        result = cursor.fetchone()
        if result is None:
            await ctx.send(f'{ctx.author.mention}, you need to register first!')
            cursor.close()
            db.close()
        else:
            cursor.execute(f"SELECT money FROM economy WHERE user_id = '{ctx.author.id}'")
            result1 = cursor.fetchone()
            money = result1[0]
            # Catches: 🐡, 🐟, 🐠, 🦀, 🐙
            # Rare Catches: 🦈, 🐬
            # Very Rare Catches: 🐳
            # Junk: 👢, 🛒, 📎, 🚫
            types=[1, 2, 3, 4] #1 = normal, 2=rare, 3=very rare, 4=junk
            weights=[0.4, 0.185, 0.005, 0.21]
            selectedType = choices(types, weights)
            if selectedType[0] == 1:
                catches = ['🐡', '🐟', '🐠', '🦀', '🐙']
                catch = random.choice(catches)
                weight = random.uniform(0.5, 1.5)
                weight = round(weight, 3)
                value = weight * 9.87
                value = round(value, 3)
            elif selectedType[0] == 2:
                catches = ['🦈', '🐬']
                catch = random.choice(catches)
                weight = random.uniform(3.0, 5.0)
                weight = round(weight,3)
                value = weight * 2.64
                value = round(value, 3)
            elif selectedType[0] == 3:
                catch = '🐳'
                weight = random.uniform(8.0, 10.0)
                weight = round(weight, 3)
                value = weight * 6
                value = round(value, 3)
            elif selectedType[0] == 4:
                catches = ['👢', '🛒', '📎', '🚫']
                catch = random.choice(catches)
                weight = 1
                value = 2
            cursor.execute(f"SELECT inventory FROM economy WHERE user_id = '{ctx.author.id}'")
            result = cursor.fetchone()
            userInventory = result[0]
            if userInventory != " ":
                userInventory = userInventory.split(',')
                for item in userInventory:
                    value *= economyInfo[item]["multiplier"]
            else:
                pass
            value = round(value, 3)
            sql = ("UPDATE economy SET money = ? WHERE user_id = ?")
            val = (float(money) + value, str(ctx.author.id))
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()
            await ctx.send(f"🎣 | You caught a {catch}, weighing {round(weight,3)}g with a value of **{value} 💠!**")
            return
    
    @commands.command(aliases=['daily'])
    @commands.guild_only()
    async def dailies(self, ctx):
        """
        Get your free daily 500 dollars. (Must be registered)
        """
        today = datetime.today()
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT user_id FROM economy WHERE user_id = '{ctx.author.id}'")
        result = cursor.fetchone()
        if result is None:
            await ctx.send('You need to register first!')
        else:
            cursor.execute(f"SELECT user_id, money, nextDaily FROM economy WHERE user_id = '{ctx.author.id}'")
            result1 = cursor.fetchone()
            nextDaily = result1[2]
            nextDaily = datetime.strptime(nextDaily, '%Y-%m-%d %H:%M:%S.%f')
            money = result1[1]
            if nextDaily < today:
                endDate = today + timedelta(days=1)
                #immediately store when next day is
                sql = (f"UPDATE economy SET nextDaily = ? WHERE user_id = ?")
                val = (endDate, str(ctx.author.id))
                cursor.execute(sql, val)
                db.commit()
                #getting inv
                cursor.execute(f"SELECT user_id, inventory FROM economy WHERE user_id = '{ctx.author.id}'")
                result = cursor.fetchone()
                userInventory = result[1]
                value=250
                #checking if user inventory is empty
                if userInventory != " ":
                    userInventory = userInventory.split(',')
                    for item in userInventory:
                        value *= economyInfo[item]["multiplier"]
                else:
                    pass
                #update
                sql = (f"UPDATE economy SET money = ? WHERE user_id = ?")
                val = (float(money) + value, str(ctx.author.id))
                cursor.execute(sql, val)
                db.commit()
                cursor.close()
                db.close()

                embed = discord.Embed(title='Daily Credits Obtained!', color=ctx.message.author.color)
                embed.add_field(name='You have withdrawn your daily allowance.', value=f'{value} 💠 has been added to your account.')
                await ctx.send(embed=embed)
                return
            else:
                trueNextDaily = nextDaily-today
                trueNextDaily = datetime.strptime(str(trueNextDaily), '%H:%M:%S.%f')
                hours = trueNextDaily.hour
                minutes = trueNextDaily.minute
                embed=discord.Embed(title='Not yet!', color=ctx.message.author.color)
                embed.add_field(name='You can\'t withdraw yet!', value=f'You need to wait {hours} hours and {minutes} minutes')
                await ctx.send(embed=embed)
                cursor.close()
                db.close()
                return
    
    @commands.command()
    @commands.guild_only()
    async def shop(self, ctx):
        """
        Display the shop.
        """
        shop = ShopMenu()
        await shop.start(ctx)

    @commands.command()
    @commands.guild_only()
    async def buy(self, ctx, item):
        """
        Buy a badge from the shop (Must be registered)
        """
        item = " "+item
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT user_id FROM economy WHERE user_id = '{ctx.author.id}'")
        result = cursor.fetchone()
        if result is None:
            await ctx.send(f"You need to register first, {ctx.author.mention}!")
            cursor.close()
            db.close()
        else:
            cursor.execute(f"SELECT user_id, inventory, money FROM economy WHERE user_id = '{ctx.author.id}'")
            result1 = cursor.fetchone()
            balance = result1[2]
            userInventory = result1[1]
            for i in range(0, len(economyInfo)):
                if item not in economyInfo.keys():
                    return await ctx.send(f"{ctx.author.mention}, that isn't a valid item!")
                if item in userInventory: # if the user owns the item
                    return await ctx.send(f"{ctx.author.mention}, you already own this item!")
                if float(balance) < economyInfo[item]["price"]:
                    return await ctx.send('You don\'t have enough money to buy this!')
                else:
                    if userInventory == " ": #if user inventory is empty
                        updatedInventory = "{}".format(item)
                    else:
                        updatedInventory = userInventory + f",{item}"
                    #deduct money
                    sql = (f"UPDATE economy SET money = ? WHERE user_id = ?")
                    val = (float(balance) - economyInfo[item]["price"], str(ctx.author.id))
                    cursor.execute(sql, val)
                    #update inventory
                    sql = (f"UPDATE economy SET inventory = ? WHERE user_id = ?")
                    val = (updatedInventory, str(ctx.author.id))
                    cursor.execute(sql, val)
                    #save and close
                    db.commit()
                    cursor.close()
                    db.close()

                    return await ctx.send(f'You now own{item}, you can see it in your inventory!')

    @commands.command()
    @commands.guild_only()
    async def baltop(self, ctx):
        """
        Get a list of the people with the most money
        """
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute("SELECT * FROM economy ORDER BY money DESC")
        data = cursor.fetchall()
        i=0
        msg = ""
        yourPos = ""
        userFound = False
        message = await ctx.send("fetching data... if this takes a long time then we are being rate limited")
        for user in data:            
            i+=1
            member = self.bot.get_user(int(user[0]))
            if member is None:
                member = await self.bot.fetch_user(int(user[0]))
            money = user[1]
            if str(ctx.author.id) == user[0]:
                yourPos = f"**{i}**.  {ctx.author} — **{round(money, 3)}**💠"
                userFound = True
            if i <= 20:
                msg += f"__{i}__. | {member} — **{round(money, 3)}**💠\n"
        if userFound is False:
            yourPos = f"{ctx.author} - **Unranked**"
        msg += "\n{}".format(yourPos)
        embed = discord.Embed(color=0xffed9e, description=msg)
        await message.edit(embed=embed)

    @commands.command(aliases=['slot'])
    @commands.cooldown(1, 15, commands.BucketType.user)
    @commands.guild_only()
    async def slots(self, ctx, money=1):
        """
        Take your chances and win big money
        """
        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()
        cursor.execute(f"SELECT money FROM economy WHERE user_id = {ctx.author.id}")
        result = cursor.fetchone()
        if result is None: #user hasn't registered
            db.close()
            cursor.close()
            return await ctx.send(f"{ctx.author.mention}, you haven't registered yet!")
        else:
            #check if they have the money
            balance = result[0]
            if balance < money:
                db.close()
                cursor.close()
                return await ctx.send(f"{ctx.author.mention}, you can't afford this!")
            
            #take the money
            sql = ("UPDATE economy SET money = ? WHERE user_id = ?")
            val = (result[0]-money, ctx.author.id)
            cursor.execute(sql, val)
            db.commit() #save

            possibleEmojis = ['🍌','🍇','🍒','🔔','🍈','💎','🍉','🍊','🍐','🎰']
            message = await ctx.send("Rolling...")
            
            for i in range(0, 3):
                slotEmojis = []
            
                for j in range(0, 9):    
                    rand = numpy.random.choice(a=numpy.arange(0,10), p=[0.15, 0.15, 0.05, 0.15, 0.15, 0.05, 0.075, 0.1, 0.1, 0.025])
                    slotEmojis.append(possibleEmojis[rand])
            
                msg ="**[(  SLOTS  )]**\n-----------------\n"
                k = 1
            
                for emoji in slotEmojis:
                    msg += f"{emoji} : "
                    if k % 3 == 0:
                        msg = msg[:-2]
                        if k == 6:
                            msg += ' **<-**'
                        msg += '\n'
                    k+=1
                msg += '----------------'
            
                await asyncio.sleep(1)
                await message.edit(content=msg)

            #calculate money
            value=0
            jackpot=False
            relevantSlots = []
            relevantSlots.extend([slotEmojis[3], slotEmojis[4], slotEmojis[5]])
            multipliers = { 2: {"🍌":0,"🍒":2,"🍐":3,"🍈":3,"🍇":3,"🍊":3,"🍉":3,"💎":10,"🎰":50},
                            3:{"🍌":1,"🍒":10,"🍐":10,"🍈":10,"🍇":10,"🍊":10,"🍉":10,"🔔":75,"💎":75,"🎰":200}}
            
            itemCount = relevantSlots.count(relevantSlots[0])
            if itemCount == 1:
                itemCount = relevantSlots.count(relevantSlots[1])
                if itemCount == 1: #at this point there cannot be any more possible winning combinations, so we say they lost money
                    pass #value is already 0
                else:
                    #item count >= 2
                    if multipliers[itemCount][relevantSlots[1]] == 0:
                        pass #they got 2 bananas, worthless, so value stays at 0
                    else:
                        value = money
                        value *= multipliers[itemCount][relevantSlots[1]]
            else:
                if multipliers[itemCount][relevantSlots[1]] == 0:
                    pass #they got 2 bananas, worthless, so value stays at 0
                else:
                    value = money
                    value *= multipliers[itemCount][relevantSlots[1]]
                    if multipliers[itemCount][relevantSlots[1]] == 200:
                        jackpot = True

            sql = ("UPDATE economy SET money = ? WHERE user_id = ?")
            val = (balance, str(ctx.author.id))
            db.commit()
            cursor.close()
            db.close()
            if value > 0 and jackpot is False:
                msg+=f'\n**{ctx.author.name}** spent **{money}** 💠 and made **{value}** 💠'
            elif jackpot is True:
                msg+=f'\n**{ctx.author.name}** spent **{money}** 💠 and 🎉🎰**__WON THE JACKPOT__**🎰🎉'
            else:
               msg+=f'\n**{ctx.author.name}** spent **{money}** 💠 and lost it all :('
            await asyncio.sleep(1)
            await message.edit(content=msg)
            


def setup(client):
    client.add_cog(Economy(client))
    now = datetime.now()
    print(f'{now} | Loaded economy module.')
