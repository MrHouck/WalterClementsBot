import ast
import discord
import datetime
from discord.ext import commands


class Eval(commands.Cog):

    def __init__(self, client):
        self.bot = client


    def insert_returns(self, body):
        # insert return stmt if the last expression is a expression statement
        if isinstance(body[-1], ast.Expr):
            body[-1] = ast.Return(body[-1].value)
            ast.fix_missing_locations(body[-1])

        # for if statements, we insert returns into the body and the orelse
        if isinstance(body[-1], ast.If):
            self.insert_returns(body[-1].body)
            self.insert_returns(body[-1].orelse)

        # for with blocks, again we insert returns into the body
        if isinstance(body[-1], ast.With):
            self.insert_returns(body[-1].body)


    @commands.command(aliases=['eval'])
    @commands.is_owner()
    async def eval_fn(self, ctx, *, cmd):
        """Evaluates input. """
        #globals
        #bot - bot instance
        #discord - discord module
        #commands - the discord.ext.commands module
        #ctx - the context
        #__import__ - the builtin __import__ function 
        fn_name = "_eval_expr"

        cmd = cmd.strip("` ")

        # add a layer of indentation
        cmd = "\n".join(f"    {i}" for i in cmd.splitlines())

        # wrap in async def body
        body = f"async def {fn_name}():\n{cmd}"

        parsed = ast.parse(body)
        body = parsed.body[0].body

        self.insert_returns(body)

        env = {
            'bot': ctx.bot,
            'discord': discord,
            'commands': commands,
            'ctx': ctx,
            '__import__': __import__
        }
        exec(compile(parsed, filename="<ast>", mode="exec"), env)

        result = (await eval(f"{fn_name}()", env))
        await ctx.send(result)

def setup(client):
    client.add_cog(Eval(client))
    now = datetime.datetime.now()
    print(f"{now} | Loaded eval module.")