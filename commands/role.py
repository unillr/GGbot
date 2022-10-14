from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands


@commands.hybrid_command()
@app_commands.describe(role='付けたい/外したいロール')
async def role(ctx, role: Optional[discord.Role]):
    '''自分のロールの追加/削除'''
    if role is None:
        category = {"PC": 0xff0000, "Mobile": 0x00ff00, "Console": 0x0000ff, "Others": 0xffffff}
        embed = discord.Embed(title='Role List', colour=discord.Colour.blurple())
        for platform, colour in category.items():
            categorized_roles = [str(r) for r in ctx.guild.roles if r.colour.value == colour]
            embed.add_field(name=platform, value='\n'.join(categorized_roles))
        await ctx.send(embed=embed, ephemeral=True)
        return
    
    if ctx.author.get_role(role.id) is None:
        await ctx.author.add_roles(role)
        await ctx.send(f'{ctx.author.display_name}が{role}の仲間になったよ!')
    else:
        await ctx.author.remove_roles(role)
        await ctx.send(f'{ctx.author.display_name}が{role}から去ったよ!')


async def setup(bot):
    bot.add_command(role)
