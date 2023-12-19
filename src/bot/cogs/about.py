import asyncio

import nextcord
from nextcord.ext import commands


# Views
class AboutView(nextcord.ui.View):
    '''A view that provides info about the bot'''

    def __init__(self):
        super().__init__(timeout=None)


# Cog
class About(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def about(self, ctx: commands.Context):
        '''Shows info about the bot'''
        await ctx.message.delete()


# Run
def setup(bot: commands.Bot):
    bot.add_cog(About(bot))
    return