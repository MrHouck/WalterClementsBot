import discord
import json
import asyncio
import random
import datetime
import sqlite3
from datetime import *
from random import choices
from discord.ext import commands

class Economy(commands.Cog):
    def __init__(self, client):
        self.bot = client

    @commands.command(aliases=['bal', 'balance'])
    @commands.guild_only()
    async def stats(self, ctx, member : discord.Member=None):
        """
        Get economy statistics of yourself or another user. The user must be registered.
        """
        member = ctx.author if not member else member
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT user_id FROM economy WHERE guild_id = '{ctx.guild.id}' and user_id = '{member.id}'")
        result = cursor.fetchone()
        if result is None:
            await ctx.send('That user has not registered!')
            cursor.close()
            db.close()
        else:
            cursor.execute(f"SELECT user_id, money, badges FROM economy WHERE guild_id = '{ctx.guild.id}' and user_id = '{member.id}'")
            result1 = cursor.fetchone()
            userBalance = result1[1]
            userBadges = result1[2]
            userBadges = userBadges.replace(',', ' ')
            embed = discord.Embed(color=member.color, timestamp=ctx.message.created_at) #using the members top role color
            embed.set_thumbnail(url=member.avatar_url) #getting the tagged members picture and setting it as the thumbnail
            embed.set_author(name=f'Economy Stats - {member}')
            embed.add_field(name='Balance:', value=f'{userBalance} 💠', inline=False) #adding the users balance
            embed.add_field(name='Badges:', value=f'{userBadges}', inline=False) #adding the badges
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
        cursor.execute(f"SELECT user_id FROM economy WHERE guild_id = '{ctx.guild.id}' and user_id = '{ctx.author.id}'")
        result = cursor.fetchone()
        if result is None:
            today = datetime.today()
            currentDay = today.day
            sql = ("INSERT INTO economy(guild_id, user_id, money, badges, nextDaily) VALUES(?, ?, ?, ?, ?)")
            val = (ctx.guild.id, ctx.author.id, 100, "\u200b", currentDay)
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()
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
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    async def fish(self, ctx):
        """
        Fish for different rarities of fish. (Must be registered)
        """
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT user_id FROM economy WHERE guild_id = '{ctx.guild.id}' and user_id = '{ctx.author.id}'")
        result = cursor.fetchone()
        if result is None:
            await ctx.send(f'{ctx.author.mention}, you need to register first!')
            cursor.close()
            db.close()
        else:
            cursor.execute(f"SELECT user_id, money FROM economy WHERE guild_id = '{ctx.guild.id}' and user_id = '{ctx.author.id}'")
            result1 = cursor.fetchone()
            money = result1[1]
            # Catches: 🐡, 🐟, 🐠, 🦀, 🐙
            # Rare Catches: 🦈, 🐬
            # Very Rare Catches: 🐳
            # Junk: 👢, 🛒, 📎, 🚫
            types=[1, 2, 3, 4] #1 = normal, 2=rare, 3=very rare, 4=junk
            weights=[0.4, 0.185, 0.015, 0.2]
            selectedType = choices(types, weights)
            if selectedType[0] == 1:
                catches = ['🐡', '🐟', '🐠', '🦀', '🐙']
                catch = random.choice(catches)
                weight = random.uniform(0.5, 2.0)
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
            cursor.execute(f"SELECT user_id, badges FROM economy WHERE guild_id = '{ctx.guild.id}' and user_id = '{ctx.author.id}'")
            result = cursor.fetchone()
            userBadges = result[1]
            if '💵' in userBadges:
                value *= 1.1
            elif '💸' in userBadges:
                value *= 1.5
            elif '💳' in userBadges:
                value *= 2.0
            elif '💰' in userBadges:
                value *= 2.5
            elif '📈' in userBadges:
                value *= 2.75
            elif '💎' in userBadges:
                value *= 3.5
            elif '😳' in userBadges:
                value *= 5.0
            elif '⭐' in userBadges:
                value *= 10.0

            value = round(value, 3)
            sql = ("UPDATE economy SET money = ? WHERE guild_id = ? and user_id = ?")
            val = (str(float(money) + value), str(ctx.guild.id), str(ctx.author.id))
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
        currentDay = today.day
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT user_id FROM economy WHERE guild_id = '{ctx.guild.id}' and user_id = '{ctx.author.id}'")
        result = cursor.fetchone()
        if result is None:
            await ctx.send('You need to register first!')
        else:
            cursor.execute(f"SELECT user_id, money, nextDaily FROM economy WHERE guild_id = '{ctx.guild.id}' and user_id = '{ctx.author.id}'")
            result1 = cursor.fetchone()
            nextDaily = result1[2]
            money = result1[1]
            if nextDaily <= currentDay:
                endDate = today + timedelta(days=1)
                endDate = endDate.day
                sql = (f"UPDATE economy SET nextDaily = ? WHERE guild_id = ? and user_id = ?")
                val = (endDate, str(ctx.guild.id), str(ctx.author.id))
                cursor.execute(sql, val)
                db.commit()
                sql = (f"UPDATE economy SET money = ? WHERE guild_id = ? and user_id = ?")
                val = (str(float(money) + 500), str(ctx.guild.id), str(ctx.author.id))
                cursor.execute(sql, val)
                db.commit()
                cursor.close()
                db.close()
                embed = discord.Embed(title='Daily Credits Obtained!', color=ctx.message.author.color)
                embed.add_field(name='You have withdrawn your daily allowance.', value='500 💠 has been added to your account.')
                await ctx.send(embed=embed)
                return
            else:
                embed=discord.Embed(title='Not yet!', color=ctx.message.author.color)
                embed.add_field(name='You can\'t withdraw yet!', value='You need to wait for the next day.')
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
        embed = discord.Embed(title='--Shop--',color=ctx.author.color)
        embed.add_field(name='💵 - 1000 💠', value='Gain 1.1x extra from fishing.', inline=True)
        embed.add_field(name='💸 - 5000 💠', value='Gain 1.5x extra from fishing.', inline=True)
        embed.add_field(name='💳 - 15000 💠', value='Gain 2.0x extra from fishing.', inline=True)
        embed.add_field(name='💰 - 25000 💠', value='Gain 2.5x extra from fishing.', inline=True)
        embed.add_field(name='📈 - 50000 💠', value='Gain 2.75x extra from fishing.', inline=True)
        embed.add_field(name='💎 - 150000 💠', value='Gain 3.5x extra from fishing.', inline=True)
        embed.add_field(name='😳 - 500000 💠', value='Gain 5x extra from fishing.', inline=True)
        embed.add_field(name='⭐ - 1000000 💠', value='Gain 10x extra from fishing.', inline=True)
        await ctx.send(embed=embed)
        return

    @commands.command()
    @commands.guild_only()
    async def buy(self, ctx, badge):
        """
        Buy a badge from the shop (Must be registered)
        """
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT user_id FROM economy WHERE guild_id = '{ctx.guild.id}' and user_id = '{ctx.author.id}'")
        result = cursor.fetchone()
        if result is None:
            await ctx.send(f"You need to register first, {ctx.author.mention}!")
            cursor.close()
            db.close()
        else:
            badges = ['💵', '💸', '💳', '💰', '📈', '💎', '😳', '⭐']
            isBadge = False
            isBadgeOwned = False
            cursor.execute(f"SELECT user_id, badges, money FROM economy WHERE guild_id = '{ctx.guild.id}' and user_id = '{ctx.author.id}'")
            result1 = cursor.fetchone()
            balance = result1[2]
            userBadges = result1[1]
            for i in range(0, len(badges)):
                if badges[i] in badge: #if the badge the user entered exists
                    isBadge = True
                    if i==0:
                        cost=1000
                    elif i==1:
                        cost=5000
                    elif i==2:
                        cost=15000
                    elif i==3:
                        cost=25000
                    elif i==4:
                        cost=50000
                    elif i==5:
                        cost=150000
                    elif i==6:
                        cost=500000
                    elif i==7:
                        cost=1000000
                if badge in userBadges: # if the user owns the badge
                    isBadgeOwned = True
            if isBadge and isBadgeOwned == False: #if the user doesn't own the existing badge
                if float(balance) < cost:
                    await ctx.send('You don\'t have enough money to buy this!')
                else:
                    if userBadges == '\u200b':
                        updatedBadges = f"{badge}"
                    else:
                        updatedBadges = userBadges + f", {badge}"
                    sql = (f"UPDATE economy SET money = ? WHERE guild_id = ? and user_id = ?")
                    val = (str(int(float(balance) - cost)), str(ctx.guild.id), str(ctx.author.id))
                    cursor.execute(sql, val)
                    sql = (f"UPDATE economy SET badges = ? WHERE guild_id = ? and user_id = ?")
                    val = (updatedBadges, str(ctx.guild.id), str(ctx.author.id))
                    cursor.execute(sql, val)
                    db.commit()
                    cursor.close()
                    db.close()
                    await ctx.send(f'You now own the {badge} badge!')
            else:
                cursor.close()
                db.close()
                if isBadgeOwned==True:
                    await ctx.send('You already own this badge!')
                else:
                    await ctx.send('This is not a valid badge!')

def setup(client):
    client.add_cog(Economy(client))
    now = datetime.now()
    print(f'{now} | Loaded economy module.')
