import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from googletrans import Translator
from googletrans import LANGCODES
from googletrans import LANGUAGES
import random
import sys
import pyjokes
import requests
import os

sys.path.append('/Users/Nathan/WalterClementsBotTest/')
import words

trans = Translator()
class Fun(commands.Cog):
    def __init__(self, client):
        self.bot = client

    @commands.command()
    @commands.guild_only()
    async def walter(self, ctx):
        await ctx.trigger_typing()
        await ctx.send("w̴̨̖̮̙̓͌ä̴̡̤̰̞ĺ̵̛̻̓͆ẗ̷̨͕̻̭͠͠ĕ̵̙̘̣ͅr̴̨̦͈̃")

    @commands.command()
    @commands.guild_only()
    async def fbi(self, ctx, *, message):
        await ctx.trigger_typing()
        arguments = message.split('|')

        image = Image.open('/Users/Nathan/WalterClementsBotTest/cogs/blankfbitemplate.jpg')
        font_type = ImageFont.truetype('/Windows/Fonts/Arial.ttf', 35)
        draw = ImageDraw.Draw(image)
        draw.text(xy=(50, 155),text=arguments[0],fill=(0,0,0),font=font_type)
        if len(arguments) == 2:
            draw.text(xy=(40, 445),text=arguments[1],fill=(0,0,0),font=font_type)
        buffer = BytesIO()
        image.save(buffer, 'jpeg')
        buffer.seek(0)
        await ctx.send(file=discord.File(buffer, filename="fbi-command-result.png"))

    @commands.command(aliases=['ach'])
    @commands.guild_only()
    async def achievement(self, ctx, *, message):
        await ctx.trigger_typing()
        if message == 'list':
            embed = discord.Embed()
            embed.add_field(name="Blocks", value="stone, wooden plank, grass, furnace, chest, crafting table, bed, sign, wooden door, iron door, rail, tnt, cobweb", inline=False)
            embed.add_field(name="Items", value="coal, iron, gold, diamond, book, redstone, bow, arrow, iron sword, diamond sword, iron chestplate, diamond chestplate, flint and steel, fire, bucket, water bucket, lava bucket, milk bucket", inline=False)
            embed.add_field(name="Misc", value="cookie, cake, pig, creeper, spawn egg, potion, splash potion", inline=False)
            await ctx.send(embed=embed)
            return
        info = message.replace(' ', '+')
        info = info.replace('+|+', '|')
        info = info.split('|')
        if len(info) != 3:
            await ctx.send('**Invalid use!** You forgot to add an achievement name!')
        else:
            msg = info[0]
            block = info[1]
            name = info[2]
            if block == 'stone':
                bNum = 20
            elif 'grass' in block:
                bNum = 1
            elif 'wooden+plank' in block:
                bNum = 21
            elif 'crafting+table' in block:
                bNum = 13
            elif 'furnace' in block:
                bNum = 18
            elif 'chest' in block:
                bNum = 17
            elif 'bed' in block:
                bNum = 9
            elif block == 'coal':
                bNum = 31
            elif block == 'iron':
                bNum = 22
            elif block == 'gold':
                bNum = 23
            elif block == 'diamond':
                bNum = 2
            elif 'sign' in block:
                bNum = 11
            elif 'book' in block:
                bNum = 19
            elif 'wooden+door' in block:
                bNum = 24
            elif 'iron+door' in block:
                bNum = 25
            elif 'redstone' in block:
                bNum = 14
            elif 'rail' in block:
                bNum = 12
            elif 'bow' in block:
                bNum = 33
            elif 'arrow' in block:
                bNum = 34
            elif 'iron+sword' in block:
                bNum = 32
            elif 'diamond+sword' in block:
                bNum = 3
            elif block == 'iron+chestplate':
                bNum = 35
            elif block == 'diamond+chestplate':
                bNum = 26
            elif 'tnt' in block:
                bNum = 6
            elif block == 'flint+and+steel':
                bNum = 27
            elif block == 'fire':
                bNum = 15
            elif block == 'bucket':
                bNum = 36
            elif 'water+bucket' in block:
                bNum = 37
            elif 'lava+bucket' in block:
                bNum = 38
            elif 'cookie' in block:
                bNum = 7
            elif 'cake' in block:
                bNum = 10
            elif 'milk+bucket' in block:
                bNum = 39
            elif 'creeper' in block:
                bNum = 4
            elif 'pig' in block:
                bNum = 5
            elif 'spawn+egg' in block:
                bNum = 30
            elif 'heart' in block:
                bNum = 8
            elif 'cobweb' in block:
                bNum = 16
            elif block == 'potion':
                bNum = 28
            elif 'splash+potion' in block:
                bNum = 29
            else:
                await ctx.send("Invalid item! Type **+achievement list** to get a list of acceptable items.")
            embed = discord.Embed()
            url = f'https://minecraftskinstealer.com/achievement/{bNum}/{name}%21/{msg}'
            embed.set_image(url=url)
            #embed.set_thumbnail(url=f'https://minecraftskinstealer.com/achievement/{bNum}/{name}%21/{msg}')
            await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def say(self, ctx, *, message):
        msg = message
        msg = msg.replace('@', ' ')
        await ctx.channel.purge(limit=1)
        await ctx.send(msg)

    @commands.command(aliases=['owo'])
    @commands.guild_only()
    async def uwu(self, ctx, *, message):
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

    @commands.command()
    @commands.guild_only()
    async def norris(self, ctx):
        joke = pyjokes.get_joke(category='chuck')
        await ctx.send(joke)

    @commands.command(aliases=['cock', 'dick', 'schlong'])
    @commands.guild_only()
    async def penis(self, ctx, member : discord.Member=None):
        member = ctx.author if not member else member
        uid = member.id
        if uid == 250067504641081355:
            embed = discord.Embed(title="Oh shit, oh fuck!", color=member.color)
            embed.add_field(name='Your cock size is too big to even begin to fathom!', value='\u200b')
            return await ctx.send(embed=embed)
        random.seed(uid)
        randomNum = randint(1, 20)
        the_string = "8"+("="*randomNum)+"D"
        if randomNum >= 15:
            theTitle = "Holy shit! Your penis is huge! Your cock size:"
        elif randomNum < 5:
            theTitle = "Damn, you have a small penis. Your cock size:"
        else:
            theTitle = "Your cock size:"
        embed = discord.Embed(title=theTitle, color=member.color)
        embed.add_field(name='\u200b', value=f'```{the_string}```')
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def retard(self, ctx, *, message):
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
        await ctx.trigger_typing()
        """
        Generate a completely random sentence.
        """
        name = random.choice(words.names)
        name = name.capitalize()
        adjective = random.choice(words.adjectives)
        verb = random.choice(words.verbs)
        adverb = random.choice(words.adverbs)
        noun =  random.choice(words.nouns)
        await ctx.send(f"{name} {verb}s the {adjective} {noun} {adverb}")


    @commands.command(aliases=['8ball'])
    @commands.guild_only()
    async def _8ball(self, ctx, *, question):
        await ctx.trigger_typing()
        """
        Consult the magic 8 ball with your question.
        """
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
        await ctx.trigger_typing()
        """
        Generate a completey random username.
        """
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
        await ctx.author.edit(nick=f'{name}{word1}{word2}{number}')
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def translate(self, ctx, *, phrase):
        await ctx.trigger_typing()
        """
        Translate a phrase from any language into english. This uses google's translation API, so it might not be 100% accurate.
        """
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

def setup(client):
    client.add_cog(Fun(client))
    print('Loaded fun module.')
