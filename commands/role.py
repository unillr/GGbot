from typing import cast

import discord
from discord import app_commands
from discord.ext import commands


@commands.hybrid_command(name='role')
@commands.bot_has_guild_permissions(manage_roles=True)
@app_commands.describe(role='付けたい/外したいロール')
async def add_or_remove_role(ctx: commands.Context[commands.Bot],
                             role: discord.Role | None) -> None:
    '''自分のロールの追加/削除'''
    if role is None:
        category: dict[str, int] = {"PC": 0xff0000, "Mobile": 0x00ff00, "Console": 0x0000ff,
                                    "Others": 0xffffff}
        guild: discord.Guild = cast(discord.Guild, ctx.guild)
        embed: discord.Embed = discord.Embed(title='Role List', colour=discord.Colour.blurple())
        for platform, colour in category.items():
            categorized_roles: list[str] = [str(r) for r in guild.roles
                                            if r.colour.value == colour]
            embed.add_field(name=platform, value='\n'.join(categorized_roles))
        await ctx.send(embed=embed, ephemeral=True)
        return

    member: discord.Member = cast(discord.Member, ctx.author)
    if member.get_role(role.id) is None:
        await member.add_roles(role)
        await ctx.send(f'{ctx.author.display_name}が{role}の仲間になったよ!')
    else:
        await member.remove_roles(role)
        await ctx.send(f'{ctx.author.display_name}が{role}から去ったよ!')


async def setup(bot: commands.Bot) -> None:
    bot.add_command(add_or_remove_role)
