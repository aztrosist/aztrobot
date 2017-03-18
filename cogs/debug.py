import asyncio, contextlib, io, inspect, sys, functools, subprocess, discord
from discord.ext import commands
from .utils import checks

@contextlib.contextmanager
def stdoutIO(stdout=None):
        old = sys.stdout
        if stdout == None:
                stdout = io.StringIO()
        sys.stdout = stdout
        yield stdout
        sys.stdout = old

class Debug:
        def __init__(self, bot):
                self.bot = bot

        def clean(self, code):
                if code.startswith("```") and code.endswith("```"):
                        return "\n".join(code.split("\n")[1:-1])

                return code.strip("` \n")

        @checks.is_owner()
        @commands.command(name='debug', pass_context=True)
        async def debug_statement(self, ctx, *, content : str):
                result = None
                code = self.clean(content)
                vals = dict(
                        self=self,
                        bot=self.bot,
                        message=ctx.message,
                        ctx=ctx,
                        server=ctx.message.server,
                        channel=ctx.message.channel,
                        author=ctx.message.author,
                        code=code,
                        io=io,
                        sys=sys,
                        commands=commands,
                        discord=discord
                )
                try:
                        precompiled = compile(code, "eval.py", "eval")
                        vals["compiled"] = precompiled
                        result = eval(precompiled, vals)
                except Exception as e:
                        await self.bot.say("<:vpRedTick:257437215615877129> `{}: {}\n`".format(type(e).__name__, e))
                        return
                if inspect.isawaitable(result):
                        result = await result
                if not result is None:
                        result = str(result)
                        await self.bot.say("<:vpGreenTick:257437292820561920> Input\n`{}`\n<:vpStreaming:212789640799846400> Output\n`{}`\n".format(content, result[:1800] + "..." if len(result) > 1800 else result))

        @checks.is_owner()
        @commands.command(name='terminal')
        async def terminal_command(self, *, command : str):
                result = await self.bot.loop.run_in_executor(None, functools.partial(subprocess.run, command, stdout=subprocess.PIPE, shell=True, universal_newlines=True))
                result = result.stdout
                await self.bot.say("<:vpGreenTick:257437292820561920> Input\n`{}`\n<:vpStreaming:212789640799846400> Output\n`{}`\n".format(command, result[:1800] + "..." if len(result) > 1800 else result))

        @checks.is_owner()
        @commands.command(name='run', pass_context=True)
        async def run_code(self, ctx, *, content : str):
                code = self.clean(content)
                code = "async def coro():\n  " + "\n  ".join(code.split("\n"))
                vals = dict(
                        self=self,
                        bot=self.bot,
                        message=ctx.message,
                        ctx=ctx,
                        server=ctx.message.server,
                        channel=ctx.message.channel,
                        author=ctx.message.author,
                        io=io,
                        code=code,
                        sys=sys,
                        commands=commands,
                        discord=discord
                )
                with stdoutIO() as s:
                        try:
                                precompiled = compile(code, "exec.py", "exec")
                                vals["compiled"] = precompiled
                                result = exec(precompiled, vals)
                                await vals["coro"]()
                        except Exception as e:
                                await self.bot.say("<:vpRedTick:257437215615877129> `{}: {}\n`".format(type(e).__name__, e))
                                return
                result = str(s.getvalue())
                if not result == "":
                        await self.bot.say("<:vpGreenTick:257437292820561920> Input\n`{}`\n<:vpStreaming:212789640799846400> Output\n`{}`\n".format(content, result[:1800] + "..." if len(result) > 1800 else result))

def setup(bot):
        bot.add_cog(Debug(bot))
