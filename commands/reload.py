from discord import app_commands
from discord.ext import commands


@commands.hybrid_command()
@commands.is_owner()
@app_commands.describe(command='リロードするコマンド')
async def reload(ctx, command: str):
    '''コマンドをリロード(開発用)'''
    await ctx.bot.reload_extension('commands.' + command)
    await ctx.send('Successfully reloaded.', ephemeral=True)

async def setup(bot):
    bot.add_command(reload)
