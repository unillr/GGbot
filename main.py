import asyncio
import os

import discord
from discord.ext import commands


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
    commands = [file[:-3] for file in os.listdir(f'./commands') if file.endswith('.py')]
    for command in commands:
        await bot.load_extension('commands.' + command)
    
    async with bot:
        await bot.start(TOKEN)

asyncio.run(main())
