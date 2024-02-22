# Library
from nextcord.ext import commands

# Internal
from src.bot.tracker import get_activity


# Views
# Cog
class Tracker(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def get_member_info(self, ctx: commands.Context):
        '''
        Gets activity info about a member and prints it to the chat. Should
        only be used by an admin.

        :param ctx: Context object to get info from
        '''
        await ctx.message.delete()

        mentions = ctx.message.mentions

        if len(mentions) != 1:
            await ctx.send('Mention exactly one member to get info about.')
            return

        member = mentions[0]
        data = get_activity(member)

        # Format the data
        formatted_data = 'User info:\n'
        for key, value in data.items():
            formatted_data += f'{key}: {value}\n'

        await ctx.send(formatted_data)


# Run
def setup(bot: commands.Bot):
    bot.add_cog(Tracker(bot))
    return
