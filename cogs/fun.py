import discord
import time
import json
import random
import sys
import requests
import os
import re
import sqlite3
import base64
import praw
import binascii
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont, ImageColor, ImageChops, ImageOps
from io import BytesIO
from urllib.request import urlopen, Request
from googletrans import Translator, LANGUAGES, LANGCODES
from datetime import datetime

sys.path.append('./')

import words

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
with open(THIS_FOLDER+'/resources/config.json', 'r') as f:
    client_data = json.load(f)
    f.close()
reddit = praw.Reddit(client_id = client_data['reddit_client_id'],
                client_secret = client_data['reddit_bot_token'],
                password= client_data['reddit_bot_password'],
                user_agent= 'desktop:Walter_Clements_Bot:v1.0.0 (by /u/MrHouck)',
                username = 'RandomImageFromSub')

trans = Translator()
class Fun(commands.Cog):
    def __init__(self, client):
        self.bot = client


    @commands.command(aliases=['reddit', 'subreddit', 'randompic', 'randomsubreddit', 'randomreddit'], usage="[subreddit]")
    @commands.guild_only()
    async def randomPicture(self, ctx, subreddit="youngpeopleyoutube"):
        """
        Get a random picture from a subreddit.
        """
        if 'r/' in subreddit:
            subreddit.strip('r/')
        subreddit = reddit.subreddit(subreddit)
        posts = subreddit.new(limit=100)
        random_post_number = random.randint(0, 100)
        for i,post in enumerate(posts):
            if i==random_post_number:
                url = "https://reddit.com"+post.permalink
                embed = discord.Embed(title=post.title, color=discord.Color.red(), url=url)
                embed.set_image(url=post.url)
        return await ctx.send(embed=embed)

    @commands.command(usage="[member]")
    @commands.guild_only()
    async def walter(self, ctx, member: discord.Member = None):
        """
        Generate a walter meme
        """
        if member is not None:
            url = member.avatar_url
            name = member.name
        else:
            url = ctx.author.avatar_url
            name = ctx.author.name

        #save the image into the buffer from the avatar url
        buffer = BytesIO()
        r = requests.get(url, allow_redirects=True)
        buffer.write(r.content)
        #open the image and resize
        buffer.seek(0)
        im = Image.open(buffer)
        im = im.resize((41, 41))
        #refresh buffer
        buffer = BytesIO()
        #create a circle mask
        bigsize = (im.size[0] * 3, im.size[1] * 3)
        mask = Image.new('L', bigsize, 0)
        #create imagedraw object
        draw = ImageDraw.Draw(mask)
        #draw an ellipse
        draw.ellipse((0, 0) + bigsize, fill=255)
        #circle cut
        mask = mask.resize(im.size, Image.ANTIALIAS)
        im.putalpha(mask)
        #fit image
        output = ImageOps.fit(im, mask.size, centering=(0.5, 0.5))
        output.putalpha(mask)
        im = output
        im = im.convert('RGBA')
        #we now have the circle image to place onto the template
        regular_font = ImageFont.truetype(THIS_FOLDER+'/resources/arial.ttf', 13)
        bold_font = ImageFont.truetype(THIS_FOLDER+'/resources/Roboto-Medium.ttf', 14)
        template = Image.open(THIS_FOLDER+'/resources/walterTemplate.png').convert('RGBA')
        #third param is alpha mask, makes it look actually ok
        template.paste(im, (9, 14), im)
        templateDraw = ImageDraw.Draw(template)
        #place the text lol
        templateDraw.text(xy=(61, 15), text=name, fill=(255,255,255), font=bold_font)
        templateDraw.text(xy=(61+9*len(name), 15), text="1 second ago", fill=(170, 170, 170), font=regular_font)
        templateDraw.text(xy=(61, 35), text=f"i like fire trucks and moster trucks \n\n\n{name}", fill=(255, 255, 255), font=regular_font)
        template.save(buffer, 'png')
        buffer.seek(0)
        await ctx.send(file=discord.File(buffer, filename="hello.png"))

    @commands.command(usage="<message>")
    @commands.guild_only()
    async def fbi(self, ctx, *, message):
        """
        Create your own FBI meme!
        """
        await ctx.trigger_typing()
        arguments = message.split('|')
        image = Image.open(THIS_FOLDER + '/resources/blankfbitemplate.jpg')
        font_type = ImageFont.truetype('/Windows/Fonts/Arial.ttf', 35)
        draw = ImageDraw.Draw(image)
        draw.text(xy=(50, 155),text=arguments[0],fill=(0,0,0),font=font_type)
        if len(arguments) == 2:
            draw.text(xy=(40, 445),text=arguments[1],fill=(0,0,0),font=font_type)
        buffer = BytesIO()
        image.save(buffer, 'jpeg')
        buffer.seek(0)
        await ctx.send(file=discord.File(buffer, filename="fbi-command-result.png"))

    @commands.command(aliases=['ach'], usage="[title] [text] [block]")
    @commands.guild_only()
    async def achievement(self, ctx, *, message=None):
        """
        Generate a minecraft achievement.
        """
        types = {
                "grass":1,"diamond":2,"diamond+sword":3,"creeper":4,"pig":5,"tnt":6,"cookie":7,"heart":8,"bed":9,"cake":10,"sign":11,"rail":12,
                "crafting+table":13,"redstone":14,"fire":15,"cobweb":16,"chest":17,"furnace":18,"book":19,"stone":20,"wooden+plank":21,"iron":22,
                "gold":23,"wooden+door":24,"iron+door":25,"diamond+chestplate":26,"flint+and+steel":27,"potion":28,"splash+potion":29,"spawn+egg":30,
                "coal":31,"iron+sword":32,"bow":33,"arrow":34,"iron+chestplate":35,"bucket":36,"water+bucket":37,"lava+bucket":38,"milk+bucket":39
                }
        await ctx.trigger_typing()
        if message == 'list':
            embed = discord.Embed()
            embed.add_field(name="Blocks", value="stone, wooden plank, grass, furnace, chest, crafting table, bed, sign, wooden door, iron door, rail, tnt, cobweb", inline=False)
            embed.add_field(name="Items", value="coal, iron, gold, diamond, book, redstone, bow, arrow, iron sword, diamond sword, iron chestplate, diamond chestplate, flint and steel, fire, bucket, water bucket, lava bucket, milk bucket", inline=False)
            embed.add_field(name="Misc", value="cookie, cake, pig, creeper, spawn egg, potion, splash potion", inline=False)
            return await ctx.send(embed=embed)
        elif message is None:
            return await ctx.send("`+achievement [[title] | [body] | [block]]`")

        info = message.replace(' ', '+')
        info = info.replace('+|+', '|')
        info = info.split('|')
        
        title = info[0]
        try:
            body = info[1]
        except IndexError:
            body = "Hello%20there!"
        try:
            block = info[2]
        except IndexError:
            block = "grass"

        body.replace(' ', '%20')
        title.replace(' ', '%20')

        if block not in types:
            return await ctx.send("Invalid item! Type **+achievement list** to get a list of acceptable items.")

        bNum = types[block]
        embed = discord.Embed()
        url = f'https://minecraftskinstealer.com/achievement/{bNum}/{title}/{body}'
        embed.set_image(url=url)
        #embed.set_thumbnail(url=f'https://minecraftskinstealer.com/achievement/{bNum}/{name}%21/{msg}')
        await ctx.send(embed=embed)

    @commands.command(usage="<message>")
    @commands.guild_only()
    async def say(self, ctx, *, message):
        """
        Make me say something!
        """
        msg = message
        msg = msg.replace('@', ' ')
        await ctx.channel.purge(limit=1)
        await ctx.send(msg)

    @commands.command(aliases=['owo'], usage="<message>")
    @commands.guild_only()
    async def uwu(self, ctx, *, message):
        """
        Make uw mehssage a wittwe mowe uwu.
        """
        await ctx.trigger_typing()
        faces = ['uwu', 'owo', ':3', '-3-', ';-;', '(づ｡◕‿‿◕｡)づ', '≧◡≦', '(o´ω｀o)', '(◡ w ◡)', '(˘ω˘)', '(ﾉ´ з `)ノ', '(//ω//)']
        output = message
        output = output.replace('@', ' ')
        output = output.replace('r', 'w')
        output = output.replace('l', 'w')
        output = output.replace('this', 'dis')
        output = output.replace('the', 'da')
        output = output.replace('you\'re', 'ure')
        output = output.replace('youre', 'ure')
        output = output.replace('your', 'ur')
        output = output.replace('me', 'meh')
        if random.randint(1,2) == 1:
            output = output.replace('you', 'u')
        else:
            output = output.replace('you', 'uwu')
        output = output.lower()
        face = random.choice(faces)
        output = output + " " + face
        await ctx.send(output)

    @commands.command(aliases=['roast'])
    @commands.guild_only()
    async def roastme(self, ctx):
        """
        Roast yourself. (There will be repeated roasts)
        """
        await ctx.trigger_typing()
        auth = ctx.author
        roasts = [
            'You must have been born on a highway, because that\'s where most accidents happen.',
            'You\'re a failed abortion whose birth certificate is an apology from the condom factory.',
            'Shut up, you\'ll never be the man your mother is.',
            'Your family tree is a cactus, because everybody on it is a prick.',
            'It looks like your face caught on fire and someone tried to put it out with a fork.',
            'Hey, you have something on your chin...3rd one down.',
            'The only thing positive in your life was the AIDS test from last year.',
            'You\'re the reason the gene pool needs a lifeguard.',
            'You\'re proof evolution can go in reverse.',
            'You\'re about as useful as a screen door on a submarine.',
            'Two wrongs don\'t make a right, take your parents as an example.',
            'Ordinarily people live and learn. You just live.',
            'That little voice in the back of your head, telling you you\'ll never be good enough? It\'s right.',
            'You\'re so fat when you turn around, people throw you a welcome back party.',
            'You must have a very low opinion of people if you think they are your equals.',
            'If your brain was made of chocolate, it wouldn\'t fill an M&M.',
            'You shouldn\t play hide and seek, no one would look for you.',
            'I tried to see things from your perspective, but I couldn\'t seem to shove my head that far up my ass.',
            'I thought of you today. It reminded me to take the garbage out.'
        ]
        roast = random.choice(roasts)
        await ctx.send(f'{auth.mention}, {roast}')

  #  @commands.command()
  #  @commands.guild_only()
  #  async def penis(self, ctx, member : discord.Member=None):
  #      member = ctx.author if not member else member
  #      uid = member.id
  #      if uid == 250067504641081355:
  #          embed = discord.Embed(title="Oh shit, oh fuck! Your cock is huge! Your cock size:", color=member.color)
  #          embed.add_field(name='```8==================================================================================================================================D```', value='\u200b')
  #          return await ctx.send(embed=embed)
  #      random.seed(uid)
  #      randomNum = randint(1, 20)
  #      the_string = "8"+("="*randomNum)+"D"
  #      if randomNum >= 15:
  #          theTitle = "Holy shit! Your penis is huge! Your cock size:"
  #      elif randomNum < 5:
  #          theTitle = "Damn, you have a small penis. Your cock size:"
  #      else:
  #          theTitle = "Your cock size:"
  #      embed = discord.Embed(title=theTitle, color=member.color)
  #      embed.add_field(name='\u200b', value=f'```{the_string}```')
  #      await ctx.send(embed=embed)

    @commands.command(aliases=['retard', 'non'], usage="<message>")
    @commands.guild_only()
    async def nonsense(self, ctx, *, message):
        """
        Takes a message you enter and mushes it into nonsense.
        """
        langs = ["af", "sq", "am", "ar", "hy", "az", "eu", "be", "bn", "bs", "bg", "ca", "ceb", "ny", "zh-CN", "zh-TW", "co", "hr", "cs", "da", "nl", "en", "eo", "et", "tl", "fi", "fr", "fy", "gl", "ka", "de", "el", "gu", "ht", "ha", "haw", "iw", "hi", "hmn", "hu", "is", "ig", "id", "ga", "it", "ja", "jw", "kn", "kk", "km", "ko", "ku", "ky", "lo", "la", "lv", "lt", "lb", "mk", "mg", "ms", "ml", "mt", "mi", "mr", "mn", "my", "ne", "no", "ps", "fa", "pl", "pt", "pa", "ro", "ru", "sm", "gd", "sr", "st", "sn", "sd", "si", "sk", "sl", "so", "es", "su", "sw", "sv", "tg", "ta", "te", "th", "tr", "uk", "ur", "uz", "vi", "cy", "xh", "yi", "yo", "zu", "fil", "hi"]
        await ctx.trigger_typing()
        msg = message
        msg = trans.translate(msg, dest=random.choice(langs))
        for i in range(0, 10):
            msg = trans.translate(msg.text, dest=random.choice(langs))
        msg = trans.translate(msg.text, dest='en')
        msg = msg.text.replace('@', '')
        await ctx.send(msg)

    @commands.command()
    @commands.guild_only()
    async def sentence(self, ctx):
        """
        Generate a completely random sentence.
        """
        await ctx.trigger_typing()
        name = random.choice(words.names)
        name = name.capitalize()
        adjective = random.choice(words.adjectives)
        verb = random.choice(words.verbs)
        adverb = random.choice(words.adverbs)
        noun =  random.choice(words.nouns)
        await ctx.send(f"{name} {verb}s the {adjective} {noun} {adverb}")


    @commands.command(aliases=['8ball'], usage="<question>")
    @commands.guild_only()
    async def eightball(self, ctx, *, question):
        """
        Consult the magic 8 ball with your question.
        """
        await ctx.trigger_typing()
        responses = [
                    "It is certain.",
                    "It is decidedly so.",
                    "Without a doubt.",
                    "Yes - definitely.",
                    "You may rely on it.",
                    "As I see it, yes.",
                    "Most likely.",
                    "Outlook good.",
                    "Yes.",
                    "Signs point to yes.",
                    "Reply hazy, try again.",
                    "Ask again later.",
                    "Better not tell you now.",
                    "Cannot predict now.",
                    "Concentrate and ask again.",
                    "Don't count on it.",
                    "My reply is no.",
                    "My sources say no.",
                    "Outlook not so good.",
                    "Very doubtful."]
        question = question.replace('@', ' ')
        embed=discord.Embed(color=0x58009f)
        embed.set_author(name="Magic 8 Ball", icon_url="https://www.horoscope.com/images-US/games/game-magic-8-ball-no-text.png")
        embed.add_field(name="Question:", value=f"{question}", inline=False)
        embed.add_field(name="Answer:", value=f"{random.choice(responses)}", inline=False)
        embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def randomname(self, ctx):
        """
        Generate a completey random username.
        """
        await ctx.trigger_typing()
        name = random.choice(words.names)
        name = name.capitalize()
        word2 = random.choice(words.nouns)
        word2 = word2.capitalize()
        word1 = random.choice(words.nouns)
        word1 = word1.capitalize()
        number = random.randint(0,99)
        embed = discord.Embed()
        embed.add_field(name="Your randomly generated username is:", value=f"{name}{word1}{word2}{number}", inline=False)
        embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(usage="<phrase>")
    @commands.guild_only()
    async def translate(self, ctx, *, phrase):
        """
        Translate a phrase from any language into english. (Might not be 100% accurate)
        """
        await ctx.trigger_typing()
        phrase = phrase.replace('@', ' ')
        t = trans.translate(phrase)
        for i in range(0,len(words.langs)):
            if t.src == words.langs[i]:
                t.src = t.src.replace(words.langs[i], words.langs2[i])
                t.src = t.src.capitalize()

        embed = discord.Embed()
        embed.add_field(name=f"Detected Language: {t.src}", value=f"{t.origin} -> {t.text}", inline=False)
        embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(aliases=["memes", "dankmeme", "dankmemes"])
    async def meme(self, ctx):
        """
        Get a random meme 
        """
        url = 'https://meme-api.herokuapp.com/gimme'
        response = urlopen(url)
        response = json.loads(response.read())
        embed = discord.Embed(title=response["title"], url=response["postLink"])
        embed.set_image(url=response["url"])
        embed.set_footer(text=f"From r/{response['subreddit']}")
        return await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def space(self, ctx):
        """
        Get information about the ISS.
        """
        url = "http://api.open-notify.org/astros.json"
        response = urlopen(url)
        result = json.loads(response.read())
        ppl = result["number"]
        embed = discord.Embed(title=f"There are currently {ppl} people in space right now.")
        people = result["people"]
        for p in people:
            name = p["name"]
            craft = p["craft"]
            embed.add_field(name=f"{name}", value=f"on board of {craft}", inline=False)
        url = "http://api.open-notify.org/iss-now.json"
        response = urlopen(url)
        result = json.loads(response.read())
        location = result["iss_position"]
        lat = location["latitude"]
        lon = location["longitude"]
        now = datetime.now()
        timestamp = now.strftime("%H:%M:%S")
        embed.set_author(name="What they see (click)", url=f"https://www.google.com/maps/@?api=1&map_action=map&center={lat},{lon}&zoom=10&basemap=satellite&layer=transit")
        embed.set_footer(text=f"(ISS @ {timestamp}) Latitude: {lat}    Longitude: {lon}")
        embed.set_thumbnail(url="https://i0.wp.com/freepngimages.com/wp-content/uploads/2015/12/international-space-station-transparent-background.png?fit=817%2C325")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def dog(self, ctx):
        """
        Get an image of a dog.
        """
        url = "https://api.thedogapi.com/v1/images/search"
        response = urlopen(url)
        result = json.loads(response.read())
        actualData = result[0]
        url = actualData["url"]
        embed = discord.Embed(color=random.randint(1, 0xfffff))
        
        embed.set_image(url=url)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        return await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def cat(self, ctx):
        """
        Get an image of a cat.
        """
        url = "https://api.thecatapi.com/v1/images/search"
        response = urlopen(url)
        result = json.loads(response.read())
        actualData = result[0]
        url = actualData["url"]
        embed = discord.Embed(color=random.randint(1, 0xfffff))
        
        embed.set_image(url=url)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        return await ctx.send(embed=embed)

    @commands.command(aliases=['birb'])
    @commands.guild_only()
    async def bird(self, ctx):
        """
        Get an image of a bird.
        """
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
        reg_url = 'https://some-random-api.ml/img/birb'
        req = Request(url=reg_url, headers=headers) 
        response = urlopen(req)
        result = json.loads(response.read())
        link = result["link"]
        embed = discord.Embed()
        embed.set_image(url=link)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        return await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def panda(self, ctx):
        """
        Get an image of a panda.
        """
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
        reg_url = 'https://some-random-api.ml/img/panda'
        req = Request(url=reg_url, headers=headers) 
        response = urlopen(req)
        result = json.loads(response.read())
        link = result["link"]
        embed = discord.Embed()
        embed.set_image(url=link)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        return await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def hug(self, ctx):
        """
        Hug gif.
        """
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
        reg_url = 'https://some-random-api.ml/animu/hug'
        req = Request(url=reg_url, headers=headers) 
        response = urlopen(req)
        result = json.loads(response.read())
        link = result["link"]
        embed = discord.Embed()
        embed.set_image(url=link)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        return await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def dogfact(self, ctx):
        """
        Get a random fact about a dog.
        """
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
        reg_url = 'https://some-random-api.ml/facts/dog'
        req = Request(url=reg_url, headers=headers) 
        response = urlopen(req)
        result = json.loads(response.read())
        fact = result["fact"]
        return await ctx.send(fact)
    
    @commands.command()
    @commands.guild_only()
    async def catfact(self, ctx):
        """
        Get a random fact about a cat.
        """
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
        reg_url = 'https://some-random-api.ml/facts/cat'
        req = Request(url=reg_url, headers=headers) 
        response = urlopen(req)
        result = json.loads(response.read())
        fact = result["fact"]
        return await ctx.send(fact)

    @commands.command()
    @commands.guild_only()
    async def koalafact(self, ctx):
        """
        Get a random fact about a koala.
        """
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
        reg_url = 'https://some-random-api.ml/facts/koala'
        req = Request(url=reg_url, headers=headers) 
        response = urlopen(req)
        result = json.loads(response.read())
        fact = result["fact"]
        return await ctx.send(fact)
    
    @commands.command()
    @commands.guild_only()
    async def pandafact(self, ctx):
        """
        Get a random fact about a panda.
        """
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
        reg_url = 'https://some-random-api.ml/facts/panda'
        req = Request(url=reg_url, headers=headers) 
        response = urlopen(req)
        result = json.loads(response.read())
        fact = result["fact"]
        return await ctx.send(fact)

def setup(client):
    client.add_cog(Fun(client))
    now = datetime.now()
    print(f'{now} | Loaded fun module.')
