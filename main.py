import asyncio
from contextlib import suppress
import os
from typing import Final

from aiohttp import web
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
bot: MyBot = MyBot(command_prefix=commands.when_mentioned_or('/'), intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    print('------')


async def main() -> None:
    extensions: list[str] = [e[:-3] for e in os.listdir('./commands') if e.endswith('.py')]
    if os.getenv('production') is None:
        extensions += ['dev.' + e[:-3] for e in os.listdir('./commands/dev') if e.endswith('.py')]

    async with bot:
        for extension in extensions:
            await bot.load_extension('commands.' + extension)
        discord.utils.setup_logging(root=False)
        await bot.start(TOKEN)


async def run_bot(_app):
    task = asyncio.create_task(main())

    yield

    task.cancel()
    with suppress(asyncio.CancelledError):
        await task


async def index(request):
    return web.Response(text="GGbot")


async def init_func():
    app = web.Application()
    app.router.add_get('/', index)
    app.cleanup_ctx.append(run_bot)

    return app
