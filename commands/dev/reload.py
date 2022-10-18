import os

from discord import app_commands
from discord.ext import commands


extensions: list[str] = [e[:-3] for e in os.listdir('./commands') if e.endswith('.py')]
if os.getenv('production') is None:
    extensions += ['dev.' + e[:-3] for e in os.listdir('./commands/dev') if e.endswith('.py')]


@commands.hybrid_command(name='reload')
@commands.is_owner()
@app_commands.describe(extension='リロードするエクステンション')
@app_commands.choices(extension=[app_commands.Choice(name=e, value=e) for e in extensions])
async def reload_extension(ctx: commands.Context[commands.Bot],
                           extension: app_commands.Choice[str]) -> None:
    '''エクステンションをリロード(開発用)'''
    await ctx.bot.reload_extension('commands.' + extension.name)
    await ctx.send('Successfully reloaded.', ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    bot.add_command(reload_extension)
