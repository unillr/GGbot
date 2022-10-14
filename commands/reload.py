from discord.ext import commands


@commands.hybrid_command()
@commands.is_owner()
async def reload(ctx, name: str):
    '''コマンドをリロード(開発用)'''
    await ctx.bot.reload_extension('commands.' + name)
    await ctx.send('Successfully reloaded.')

async def setup(bot):
    bot.add_command(reload)
