import asyncio
import os

import discord
from discord.ext import commands


MY_GUILD = discord.Object(id=os.environ['GUILD_ID'])
TOKEN = os.environ['DISCORD_TOKEN']


class MyBot(commands.Bot):
    async def setup_hook(self):
        self.tree.copy_global_to(guild=MY_GUILD)
        # self.tree.clear_commands(guild=MY_GUILD)  # 登録したコマンドを削除
        await self.tree.sync(guild=MY_GUILD)


intents = discord.Intents.all()
bot = MyBot(command_prefix=commands.when_mentioned_or('/'), intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    print('------')

async def main():
    extensions = [e[:-3] for e in os.listdir(f'./commands') if e.endswith('.py')]
    for extension in extensions:
        await bot.load_extension('commands.' + extension)
    
    async with bot:
        await bot.start(TOKEN)

asyncio.run(main())
