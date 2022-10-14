import asyncio
import os

import discord
from discord.ext import commands


COMMANDS_DIR = 'commands'
MY_GUILD = discord.Object(id=os.environ['GUILD_ID'])
TOKEN = os.environ['DISCORD_TOKEN']


class MyBot(commands.Bot):
    async def setup_hook(self):
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)


intents = discord.Intents.all()
bot = MyBot(command_prefix=commands.when_mentioned_or('/'), intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    print('------')

async def main():
    commandfiles = filter(lambda file: file.endswith('.py'), os.listdir(f'./{COMMANDS_DIR}'))
    for file in commandfiles:
        extension = COMMANDS_DIR + '.' + file.removesuffix('.py')
        await bot.load_extension(extension)
    
    async with bot:
        await bot.start(TOKEN)

asyncio.run(main())
