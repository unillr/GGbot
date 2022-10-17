from discord.ext import commands


@commands.hybrid_command()
@commands.is_owner()
async def logout(ctx):
    '''Botのログアウト(開発用)'''
    await ctx.send('Goodbye!', ephemeral=True)
    await ctx.bot.close()


async def setup(bot):
    bot.add_command(logout)
