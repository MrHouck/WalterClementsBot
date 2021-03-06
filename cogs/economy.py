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
f = open(THIS_FOLDER+'/resources/economy.json', 'r')
economyInfo = json.load(f)
f.close()
f = open(THIS_FOLDER+'/resources/emoji.json', 'r')
emojiData = json.load(f)
f.close()

def convertEmoji(emojiName : str):
    return emojiData[emojiName]

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
                embed.add_field(name="{} - {:,}".format(convertEmoji(item), economyInfo[item]['price']), value=f"Gain {economyInfo[item]['multiplier']}x as much money", inline=False)
            i += 1
        embed.set_footer(text="Multipliers add. (If you get the apple and the corn, you get a 2.2x multiplier)")
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
    @commands.command(aliases=['bal', 'balance'], usage="[member]")
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
            if userInventory == "":
                userInventory = "\u200b"
            else:
                try:
                    if userInventory == "apple":
                        userInventory = convertEmoji("apple")
                    else:
                        userInventory = userInventory.split(',')
                        temp = ""
                        for item in userInventory:
                            temp += convertEmoji(item)
                        userInventory = temp
                except:
                    pass

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
            embed.add_field(name='Balance:', value=f'{round(float(userBalance), 3)} <:coin:726193607564066888>', inline=False) #adding the users balance
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
            val = (ctx.author.id, 100, "", str(today)) 
            cursor.execute(sql, val)
            db.commit() 
            sql = ("INSERT INTO towers(user_id, toClaim, coinsPerHour, homes, groceryStores, restaurants, clothingStores, electronicsStores, factories, banks, spaceStations) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
            val = (ctx.author.id, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0)
            cursor.execute(sql, val)
            db.commit() 
            cursor.close()
            db.close()
            #send embed
            embed = discord.Embed(title='*Registered!*', color=ctx.message.author.color)
            embed.add_field(name='You have been added to the database!', value='To start off, you have been credited __100 <:coin:726193607564066888>__.')
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
            #(1) Catches: 🐟
            #(2) Rare Catches: 🐠
            #(3) Very Rare Catches: 🐳
            #(4) Exotic Catches: 🐙, 🐬, 🦀
            #(5) Junk: 👢, 🛒, 📎, 🚫
            types=[1, 2, 3, 4, 5]
             
            weights=[.4, .1, .019, .001, .48]
            
            selectedType = choices(types, weights)

            exotic = False
            if selectedType[0] == 1:
                catch = '🐟'
                weight = random.uniform(2.0, 3.0)
                weight = round(weight, 1)
                value = weight * 9.87
                value = round(value, 1)
            elif selectedType[0] == 2:
                catch = '🐡'
                weight = random.uniform(5.0, 7.0)
                weight = round(weight,1)
                value = weight * 2.64
                value = round(value, 1)
            elif selectedType[0] == 3:
                catch = '🐠'
                weight = random.uniform(8.0, 10.0)
                weight = round(weight, 1)
                value = weight * 6
                value = round(value, 1)
            elif selectedType[0] == 4:
                exotic=True
                catches= ['🐙', '🐬', '🦀']
                weight = random.uniform(100.0, 250.0)
                weight = round(weight, 1)
                value = weight * 4
            elif selectedType[0] == 5:
                catches = ['👢', '🛒', '📎', '🚫']
                catch = random.choice(catches)
                weight = 1
                value = 3
            cursor.execute(f"SELECT inventory FROM economy WHERE user_id = '{ctx.author.id}'")
            result = cursor.fetchone()
            userInventory = result[0]
            if userInventory != " ":
                userInventory = userInventory.split(',')
                multiplier = 0
                for item in userInventory:
                    multiplier += economyInfo[item]["multiplier"]
                value *= multiplier
            else:
                pass
            value = round(value, 1)
            sql = ("UPDATE economy SET money = ? WHERE user_id = ?")
            val = (float(money) + value, str(ctx.author.id))
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()
            if exotic:
                return await ctx.send(f"🎣 | **WOW!!!** You caught an __**exotic**__ {catch}, weighing {round(weight,1)} grams with a value of **{value} <:coin:726193607564066888>!**")
            else:
                return await ctx.send(f"🎣 | You caught a {catch}, weighing {round(weight,1)} grams with a value of **{value} <:coin:726193607564066888>!**")
    
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
                    multiplier = 0
                    for item in userInventory:
                        multiplier += economyInfo[item]["multiplier"]
                    value *= multiplier
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
                embed.add_field(name='You have withdrawn your daily allowance.', value=f'{value} <:coin:726193607564066888> has been added to your account.')
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

    @commands.command(usage="<item>")
    @commands.guild_only()
    async def buy(self, ctx, item):
        """
        Buy a badge from the shop (Must be registered)
        """
        for name, ustring in emojiData.items():
            if ustring == item:
                item = name
        
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
                    if userInventory == "": #if user inventory is empty
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
                    return await ctx.send(f'You now own {convertEmoji(item)}, you can see it in your inventory!')

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
                yourPos = f"**{i}**.  {ctx.author} — **{round(money, 3)}**<:coin:726193607564066888>"
                userFound = True
            if i <= 20:
                msg += f"__{i}__. | {member} — **{round(money, 3)}**<:coin:726193607564066888>\n"
        if userFound is False:
            yourPos = f"{ctx.author} - **Unranked**"
        msg += "\n{}".format(yourPos)
        embed = discord.Embed(color=0xffed9e, description=msg)
        await message.edit(embed=embed)

    @commands.command(aliases=['slot'], usage="[money]")
    @commands.cooldown(1, 8, commands.BucketType.user)
    @commands.guild_only()
    async def slots(self, ctx, money=1):
        """
        Take your chances and win big money
        """ 
        debug = False
        if money == 80085:
            if ctx.author.id == 250067504641081355:
                debug = True
            else:
                money=80085
                await ctx.send('nice.')

        if money <= 0:
            return await ctx.send('no')
        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()
        cursor.execute(f"SELECT money FROM economy WHERE user_id = {ctx.author.id}")
        result = cursor.fetchone()
        if result is None: #user hasn't registered
            cursor.close()
            db.close()
            return await ctx.send(f"{ctx.author.mention}, you haven't registered yet!")
        else:
            #check if they have the money
            balance = result[0]
            if balance < money and debug is False:
                cursor.close()
                db.close()
                return await ctx.send(f"{ctx.author.mention}, you can't afford this!")
           
            #take the money
            if not debug:
                balance = result[0]-money


            possibleEmojis = ['🍌','🍐','🍍','🍉', '🍊', '🍈', '🍇','🍒','🥝','🍪','🍞','🧃','💎','🔔','🎰']

            message = await ctx.send("Rolling...")
            
            for i in range(0, random.randint(1, 7)):
                slotEmojis = []

                for j in range(0, 9):    
                    rand = numpy.random.choice(a=numpy.arange(0,15), p=[0.3, 0.125, 0.1, 0.09, 0.08, 0.075, 0.065, 0.045, 0.035, 0.02, 0.02, 0.015, 0.015, 0.01, 0.005])
                    slotEmojis.append(possibleEmojis[rand])
                if debug:
                    await ctx.send(slotEmojis)            
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
            if debug:
                await ctx.send(f"Relevant slots: {relevantSlots}")
            multipliers = {
                2: 
                {
                    "🍌":1.3,
                    "🍐":1.425,
                    "🍍":1.525,
                    "🍉":1.620,
                    "🍊":1.705,
                    "🍈":1.780,
                    "🍇":1.864,
                    "🍒":1.943,
                    "🥝":2,
                    "🍪":2.1,
                    "🍞":2.25,
                    "🧃":2.45,
                    "💎":2.78,
                    "🔔":3,
                    "🎰":5
                },
                3:
                {
                    "🍌":2.817,
                    "🍐":3.383,
                    "🍍":3.875,
                    "🍉":4.373,
                    "🍊":4.845,
                    "🍈":5.28,
                    "🍇":5.783,
                    "🍒":6.292,
                    "🥝":6.667,
                    "🍪":7.35,
                    "🍞":8.437,
                    "🧃":10.003,
                    "💎":12.88,
                    "🔔":15,
                    "🎰":41.667
                }
            }               
            itemCount = relevantSlots.count(relevantSlots[0])
            if itemCount == 1:
                itemCount = relevantSlots.count(relevantSlots[1])
                if itemCount == 1: #at this point there cannot be any more possible winning combinations, so we say they lost money
                    pass #value is already 0
                else:
                    value = money
                    value *= multipliers[itemCount][relevantSlots[1]]
            else:
                if multipliers[itemCount][relevantSlots[1]] == 0:
                    pass #they got 2 bananas, worthless, so value stays at 0
                else:
                    value = money
                    value *= multipliers[itemCount][relevantSlots[1]]
                    if multipliers[itemCount][relevantSlots[1]] == 41.667:
                        jackpot = True
            if debug:
                await ctx.send(itemCount)
                if itemCount > 1:
                    await ctx.send(multipliers[itemCount][relevantSlots[0]])
                    await ctx.send(multipliers[itemCount][relevantSlots[1]])
            if not debug:
                db = sqlite3.connect('main.sqlite')
                cursor = db.cursor()
                value = int(value)
                sql = ("UPDATE economy SET money = ? WHERE user_id = ?")
                val = (balance+value, str(ctx.author.id))
                cursor.execute(sql, val)
                db.commit()
                cursor.close()
                db.close()
            
            
            if value > 0 and jackpot is False:
                msg+=f'\n**{ctx.author.name}** spent **{money}** coins and won **{value}** coins'
            elif jackpot is True:
                msg+=f'\n**{ctx.author.name}** spent **{money}** coins and won **{value}** coins. **Jackpot!**'
            else:
                face = random.choice([':(', ':<', ':c', ':C', ':L', ':/', ':|', 'ಠ_ಠ', '>:[', ':{', ';(', '(._.)', ';-;', '.-.'])
                msg+=f'\n**{ctx.author.name}** spent **{money}** coins and lost it all {face}'
            await asyncio.sleep(1)
            await message.edit(content=msg)
            


def setup(client):
    client.add_cog(Economy(client))
    now = datetime.now()
    print(f'{now} | Loaded economy module.')
