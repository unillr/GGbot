import asyncio
import os
from typing import Final

import discord
from discord.ext import commands


MY_GUILD: Final = discord.Object(id=os.environ['GUILD_ID'])
TOKEN: Final = os.environ['DISCORD_TOKEN']


class MyBot(commands.Bot):
    async def setup_hook(self) -> None:
        self.tree.copy_global_to(guild=MY_GUILD)
        # self.tree.clear_commands(guild=MY_GUILD)  # 登録したコマンドを削除
        await self.tree.sync(guild=MY_GUILD)


intents: discord.Intents = discord.Intents.all()
bot: commands.Bot = MyBot(command_prefix=commands.when_mentioned_or('/'), intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    print('------')


async def main() -> None:
    extensions: list[str] = [e[:-3] for e in os.listdir('./commands') if e.endswith('.py')]
    if os.getenv('production') is None:
        extensions += ['dev.' + e[:-3] for e in os.listdir('./commands/dev') if e.endswith('.py')]
    for extension in extensions:
        await bot.load_extension('commands.' + extension)

    async with bot:
        await bot.start(TOKEN)

asyncio.run(main())
