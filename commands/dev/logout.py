from discord.ext import commands


@commands.hybrid_command()
@commands.is_owner()
async def logout(ctx: commands.Context[commands.Bot]) -> None:
    '''Botをログアウトさせる(開発用)'''
    await ctx.send('Goodbye!', ephemeral=True)
    ctx.bot.tree.clear_commands(guild=ctx.guild)
    await ctx.bot.tree.sync(guild=ctx.guild)
    await ctx.bot.close()


async def setup(bot: commands.Bot) -> None:
    bot.add_command(logout)
