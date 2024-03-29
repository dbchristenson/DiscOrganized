# General
import os
import logging

# Library
from dotenv import load_dotenv
from nextcord import Intents
from nextcord.ext import commands
import pytest

# Setup logging
logger = logging.getLogger('nextcord')
logger.setLevel(logging.DEBUG)

format = '%(asctime)s:%(levelname)s:%(name)s: %(message)s'
handler = logging.FileHandler(filename='src/bot/nextcord.log', mode='w')
handler.setFormatter(logging.Formatter(format))
logger.addHandler(handler)

# Setup bot
intents = Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or("~"),
    intents=intents
    )
MANAGER_ROLE = '728486683439398962'


@bot.command()
@commands.has_role(MANAGER_ROLE)
async def shutdown(ctx: commands.Context):
    await ctx.message.delete()
    exit()


@bot.command()
@commands.has_role(MANAGER_ROLE)
async def load(ctx: commands.Context, extension: str):
    bot.load_extension(f'cogs.{extension}')
    print(f'{extension} successfully loaded')


@bot.command()
@commands.has_role(MANAGER_ROLE)
async def unload(ctx: commands.Context, extension: str):
    bot.unload_extension(f'cogs.{extension}')
    print(f'{extension} successfully unloaded')


@bot.command()
@commands.has_role(MANAGER_ROLE)
async def reload(ctx: commands.Context, extension: str):
    bot.unload_extension(f'cogs.{extension}')
    bot.load_extension(f'cogs.{extension}')
    print(f'{extension} successfully re-loaded')
    await ctx.message.delete()


def find_cogs():
    '''Finds all cogs in the cogs folder and loads them'''
    for filename in os.listdir('src/bot/cogs'):
        check = filename.endswith('.py') and '__' not in filename

        if check:
            try:
                bot.load_extension(f'cogs.{filename[:-3]}')
            except BaseException:
                logger.warning(f'Failed to load cog: {filename}')
                continue


@bot.event
async def on_ready():
    '''Runs when the bot is initialized.'''
    logger.info(f'{bot.user.name} has connected to Discord!')

    # Load all cogs
    find_cogs()

    # Run tests
    logger.info('Running tests...')

    pytest_output = open('src/bot/pytest.log', 'w')
    pytest_args = ['tests', '--capture=sys', '--log-cli-level=INFO']
    exit_code = pytest.main([pytest_args, pytest_output])

    # Print the test summary
    pytest_output.seek(0)  # Go to the start of the StringIO buffer
    logger.info('Tests completed. Summary:\n' + pytest_output.read())

    # Check the exit code to determine if tests passed
    if exit_code == 0:
        logger.info('All tests passed.')
    else:
        logger.error('Some tests failed.')


if __name__ == '__main__':
    load_dotenv()
    token = str(os.getenv('DISCORD_TOKEN'))
    bot.run(token)
