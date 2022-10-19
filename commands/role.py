from typing import cast

import discord
from discord import app_commands
from discord.ext import commands


@app_commands.command(name='role')
@app_commands.checks.bot_has_permissions(manage_roles=True)
@app_commands.describe(role='付けたい/外したいロール')
async def add_or_remove_role(interaction: discord.Interaction,
                             role: discord.Role | None) -> None:
    '''自分のロールの追加/削除'''
    if role is None:
        category: dict[str, int] = {"PC": 0xff0000, "Mobile": 0x00ff00, "Console": 0x0000ff,
                                    "Others": 0xffffff}
        guild: discord.Guild = cast(discord.Guild, interaction.guild)
        embed: discord.Embed = discord.Embed(title='Role List', colour=discord.Colour.blurple())
        for platform, colour in category.items():
            categorized_roles: list[str] = [r.name for r in guild.roles
                                            if r.colour.value == colour]
            embed.add_field(name=platform, value='\n'.join(categorized_roles))
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

    member: discord.Member = cast(discord.Member, interaction.user)
    if member.get_role(role.id) is None:
        await member.add_roles(role)
        await interaction.response.send_message(f'{member.display_name}が{role}の仲間になったよ!')
    else:
        await member.remove_roles(role)
        await interaction.response.send_message(f'{member.display_name}が{role}から去ったよ!')


async def setup(bot: commands.Bot) -> None:
    bot.tree.add_command(add_or_remove_role)
