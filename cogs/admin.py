from discord.ext import commands
from .utils import checks
import discord
import subprocess
import sys
import os

class Admin:
    """admin stuff"""

    def __init__(self, bot):
        self.bot = bot

    @checks.is_owner()
    @commands.command()
    async def load(self, *, module : str):
        """load some shit"""
        try:
            self.bot.load_extension(module)
        except Exception as e:
            await self.bot.say('<:vpRedTick:257437215615877129> `{}: {}`'.format(type(e).__name__, e))
        else:
            await self.bot.say('<:vpGreenTick:257437292820561920>')

    @checks.is_owner()
    @commands.command()
    async def unload(self, *, module : str):
        """you are mom gay?"""
        try:
            self.bot.unload_extension(module)
        except Exception as e:
            await self.bot.say('<:vpRedTick:257437215615877129> `{}: {}`'.format(type(e).__name__, e))
        else:
            await self.bot.say('<:vpGreenTick:257437292820561920>')

    @checks.is_owner()
    @commands.command(name='reload')
    async def _reload(self, *, module : str):
        """reload a module"""
        try:
            self.bot.unload_extension('cogs.' + module)
            self.bot.load_extension('cogs.' + module)
        except Exception as e:
            await self.bot.say('<:vpRedTick:257437215615877129> `{}: {}`'.format(type(e).__name__, e))
        else:
            await self.bot.say('<:vpGreenTick:257437292820561920>')

def setup(bot):
    bot.add_cog(Admin(bot))
