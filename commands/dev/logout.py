from discord.ext import commands


@commands.hybrid_command()
@commands.is_owner()
async def logout(ctx: commands.Context[commands.Bot]) -> None:
    '''Botのログアウト(開発用)'''
    await ctx.send('Goodbye!', ephemeral=True)
    await ctx.bot.close()


async def setup(bot: commands.Bot) -> None:
    bot.add_command(logout)
