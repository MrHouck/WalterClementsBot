import discord
import json
import os
import asyncio
import random
import datetime
import sqlite3
from datetime import datetime, timedelta
from random import choices
from discord.ext import commands
from discord.ext import menus

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
economyInfo = {
            " 🍎":{"price":250,"multiplier":1.2},
            " 🌽":{"price":2250,"multiplier":1.4},
            " ⌚":{"price":6500,"multiplier":1.6},
            " 🍚":{"price":10500,"multiplier":1.8},
            " 📙":{"price":20500,"multiplier":2.0},
            " 🍒":{"price":42000,"multiplier":2.2},
            " 💙":{"price":65000,"multiplier":2.4},
            " 🛹":{"price":110000,"multiplier":2.6},
            " 🔋":{"price":220000,"multiplier":2.8},
            " ⌛":{"price":445000,"multiplier":3.0},
            " 🏅":{"price":645000,"multiplier":3.0},
            " 🐠":{"price":1000000,"multiplier":3.0},
            " 🦞":{"price":6600000,"multiplier":3.2},
            " 💵":{"price":25000000,"multiplier":3.4},
            " 💸":{"price":66000000,"multiplier":3.8},
            " 💰":{"price":22500000,"multiplier":4.0},
            " 💳":{"price":75000000,"multiplier":4.0},
            " 📈":{"price":100000000,"multiplier":4.0},
            " 💎":{"price":225000000,"multiplier":4.2},
            " 😳":{"price":500000000,"multiplier":4.4},
            " 😃":{"price":750000000,"multiplier":4.6},
            " ⭐":{"price":100000000000,"multiplier":4.8},
            " 🎉":{"price":255000000000,"multiplier":5},
            " 🤑":{"price":5000000000000,"multiplier":10}
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
            cursor.close()
            db.close()
            #send embed
            embed = discord.Embed(title='*Registered!*', color=ctx.message.author.color)
            embed.add_field(name='You have been added to the database!', value='To start off, you have been credited __100 💠__.')
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
        for user in data:            
            i+=1
            member = self.bot.get_user(int(user[0]))
            money = user[1]
            if str(ctx.author.id) == user[0]:
                yourPos = f"__{i}__. | **{ctx.author}** — {round(money, 3)} 💠"
                userFound = True
            if i <= 20:
                msg += f"__{i}__. | **{member}** — {round(money, 3)} 💠\n"
        if userFound is False:
            yourPos = f"**{ctx.author}** - Unranked"
        msg += "\n{}".format(yourPos)
        embed = discord.Embed(color=0xffed9e, description=msg)
        await ctx.send(embed=embed)





def setup(client):
    client.add_cog(Economy(client))
    now = datetime.now()
    print(f'{now} | Loaded economy module.')
