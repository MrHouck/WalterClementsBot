import discord
import sqlite3
from discord.ext import commands, tasks

class Towers(commands.Cog):
    def __init__(self, client):
        self.bot = client


    @commands.group(invoke_without_subcommand=True, aliases=["towers"])
    @commands.guild_only()
    async def tower(self, ctx):
        """
        Base command for the Towers module.
        """
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(color=discord.Color.teal(), title='<:tower:713573997538705471> Tower Commands <:tower:713573997538705471>', 
                                  description="**Basic Info**:\n- Towers is part of the economy, buy buildings which make money without you having to do anything!\n- Towers is simple, just buy different levels of the tower, and watch as your money skyrockets!\n- You can buy up to 999 of each level of the tower.\n\n**Tower Subcommands**:\n``+tower help`` - this\n``+tower view [user]`` - view your tower, or someone elses\n``+tower buy`` - buy a shop to make you money\n``+tower claim`` - Claim coins earned by your tower.")
            return await ctx.send(embed=embed)

    @tower.command()
    @commands.guild_only()
    async def view(self, ctx, member=None):
        """
        View your tower or someone elses.
        """
        if member is None:
            member = ctx.author
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM towers WHERE user_id = {member.id}")
        result = cursor.fetchone()
        if result is None: 
            if member == ctx.author:
                return await ctx.send(f"{ctx.author.mention}, you haven't registered yet!")
            else:
                return await ctx.send(f"{ctx.author.mention}, that user has not registered yet!")
        else:
            msg = f"```md\n < {member.name}'s Empire >\n"
            basePrices = {'3': 1000,'4': 4500,'5': 22500,'6': 70000,'7': 140000,'8': 475000,'9': 900000,'10': 3300000}
            toClaim = result[1]
            coinsPerHour = result[2]
            homes = result[3]
            groceryStores = result[4]
            restaurants = result[5]
            clothingStores = result[6]
            electronicsStores = result[7]
            factories = result[8]
            banks = result[9]
            spaceStations = result[10]
            if spaceStations > 0:
                msg+=f"\n# Space Station     (x{spaceStations})  ({spaceStations*3500} coins/h)  - {int(basePrices['10'] * (spaceStations+1) * 0.78)} coins each"
            else:
                msg+="\n> Space Station             (???? coins/h)   - 3,300,000 coins each"
            if banks > 0:
                msg+=f"\n# Bank              (x{banks})  ({banks*1000} coins/h)  - {int(basePrices['9'] * (banks+1) * 0.78)} coins each"
            else:
                msg+="\n> Bank                      (???? coins/h)   - 900,000 coins each"
            if  factories > 0:
                msg+=f"\n# Factory           (x{factories})  ({factories*500} coins/h)   - {int(basePrices['8'] * (factories+1) * 0.78)} coins each"
            else:
                msg+="\n> Factory                   (??? coins/h)    - 475,000 coins each"
            if electronicsStores > 0:
                msg+=f"\n# Electronics Store (x{electronicsStores})  ({electronicsStores*150} coins/h)   - {int(basePrices['7'] * (electronicsStores+1) * 0.78)} coins each"
            else:
                msg+="\n> Electronics Store         (??? coins/h)    - 140,000 coins each"
            if clothingStores > 0:
                msg+=f"\n# Clothing Store    (x{clothingStores})  ({clothingStores*75} coins/h)    - {int(basePrices['6'] * (clothingStores+1) * 0.78)} coins each"
            else:
                msg+="\n> Clothing Store            (?? coins/h)     - 70,000 coins each"
            if restaurants > 0:
                msg+=f"\n# Restaurant        (x{restaurants})  ({restaurants*25} coins/h)    - {int(basePrices['5'] * (restaurants+1) * 0.78)} coins each"
            else:
                msg+="\n> Restaurant                (?? coins/h)     - 22,500 coins each"
            if groceryStores > 0:
                msg+=f"\n# Grocery Store     (x{groceryStores})  ({groceryStores*5} coins/h)     - {int(basePrices['4'] * (groceryStores+1) * 0.78)} coins each"
            else:
                msg+="\n> Grocery Store             (? coins/h)      - 4,500 coins each"
            
            msg+=f"\n# Home Business     (x{homes})  ({homes*1} coins/h)      - {int(basePrices['3'] * (homes+1) * 0.78)} coins each"
            msg+=f"\n\nYou are making {coinsPerHour} coins per hour."
            if toClaim != 0:
                msg += f"\nYou also have {toClaim} coins waiting to be claimed.```"
            else:
                msg+="```"
            await ctx.send(msg)
    
    @tower.command()
    @commands.guild_only()
    async def buy(self, ctx, *, floor):
        """
        Buy a certain floor in Towers.
        """
        if 'ho' in floor:
            toBuy = 3
            cph = 1
        elif 'gr' in floor:
            toBuy = 4
            cph = 5
        elif 'rest' in floor:
            toBuy = 5
            cph = 25
        elif 'clo' in floor:
            toBuy = 6
            cph = 75
        elif 'ele' in floor:
            toBuy = 7
            cph = 150
        elif 'fac' in floor:
            toBuy = 8
            cph = 500
        elif 'ban' in floor:
            toBuy = 9
            cph = 1000
        elif 'spa' in floor: 
            toBuy = 10
            cph = 3500
        else:
            return await ctx.send(f"{ctx.author.mention}, that isn't a valid floor!")
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM towers WHERE user_id = {ctx.author.id}")
        #TODO: Check if user exists, add the associated coins p/h to their coins per hour, increase the amount of the level in the DB 
        result = cursor.fetchone()
        if result is None:
            return await ctx.send(f"{ctx.author.mention}, you aren't registered yet!")
        basePrices = {'3': 1000,'4': 4500,'5': 22500,'6': 70000,'7': 140000,'8': 475000,'9': 900000,'10': 3300000}
        buildings = ['','','','homes','groceryStores','restaurants','clothingStores', 'electronicsStores', 'factories', 'banks', 'spaceStations']
        buildingNames = ['','','','Home Business', 'Grocery Store', 'Restaurant', 'Clothing Store', 'Electronics Store', 'Factory', 'Bank', 'Space Station']
        building = buildings[toBuy]
        buildingName = buildingNames[toBuy]
        coinsPerHour = result[2]
        buildingCount = result[toBuy]
        if buildingCount == 0:
            price = basePrices[str(toBuy)]
        else:
            price = basePrices[str(toBuy)] * (buildingCount+1) * 0.78
        cursor.execute(f"SELECT money FROM economy WHERE user_id = {ctx.author.id}")
        result = cursor.fetchone()
        userBal = result[0]
        if userBal - price < 0:
            return await ctx.send(f"{ctx.author.mention}, you can't afford this! You need another {price-userBal} coins!")

        sql = (f"UPDATE economy SET money = ? WHERE user_id = ?")
        val = (userBal-price, ctx.author.id)
        cursor.execute(sql, val)
        db.commit()
        sql = (f"UPDATE towers SET {building} = ? WHERE user_id = ?")
        val = (buildingCount+1, ctx.author.id)
        cursor.execute(sql, val)
        sql = (f"UPDATE towers SET coinsPerHour = ? WHERE user_id = ?")
        val = (coinsPerHour+cph, ctx.author.id)
        cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()
        return await ctx.send(f"```diff\n+ Succesfully purchased 1 {buildingName}\n- Deducted {price} coins from your account. You now have {userBal-price} coins.```")
        


    
    @tower.command()
    @commands.guild_only()
    async def claim(self, ctx):
        """
        Claim coins your tycoon has generated, if any
        """
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT toClaim FROM towers WHERE user_id = {ctx.author.id}")
        result = cursor.fetchone()
        if result is None:
            return await ctx.send(f"{ctx.author.mention}, you haven't registered yet!")
        else:
            toClaim = result[0]
            if toClaim == 0:
                return await ctx.send("You don't have any money to claim!")
            cursor.execute(f"SELECT money FROM economy WHERE user_id = {ctx.author.id}")
            result = cursor.fetchone()
            balance = result[0]
            sql=(f"UPDATE economy SET money = ? WHERE user_id = ?")
            val=(balance+toClaim, ctx.author.id)
            cursor.execute(sql, val)
            db.commit()
            sql=(f"UPDATE towers SET toClaim = ? WHERE user_id = ?")
            val=(0, ctx.author.id)
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()
            return await ctx.send(f'```Successfully claimed {toClaim} coins. Your balance is now {balance+toClaim}```')

    @commands.Cog.listener()
    async def on_ready(self):
        self.update_claim.start()

    
    @tasks.loop(seconds=10)
    async def update_claim(self):
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM towers")
        data = cursor.fetchall()
        for user in data:
            user_id = user[0]
            toClaim = user[1]
            coinsPerHour = user[2]
            toClaim += coinsPerHour
            sql = ("UPDATE towers SET toClaim = ? WHERE user_id = ?")
            val = (toClaim, user_id)
            cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()









def setup(client):
    client.add_cog(Towers(client))