import os
import random

import discord
from discord.ext import commands


class MapSelectMenu(discord.ui.View):
    maps = [m[:-4] for m in os.listdir(f'./images/maps/VALORANT') if m.endswith('.png')]
    options = [discord.SelectOption(label=l) for l in maps]

    @discord.ui.select(placeholder='BAN MAPを選択…', min_values=0, max_values=len(options)-1, options=options)
    async def ban_map(self, interaction: discord.Integration, select: discord.ui.Select):
        pickedmap = random.choice([m for m in self.maps if m not in select.values])
        embed = discord.Embed(title=pickedmap, colour=discord.Colour.red())
        embed.set_image(url=f'attachment://{pickedmap}.png')
        embed.set_footer(text='BAN: ' + (' '.join(select.values) or 'なし'))
        attachment = discord.File(f'./images/maps/VALORANT/{pickedmap}.png', filename=f'{pickedmap}.png')
        await interaction.response.edit_message(embed=embed, attachments=[attachment], view=None)


@commands.hybrid_command()
async def map(ctx):
    '''VALORANTのマップをランダムに選択'''
    await ctx.send(view=MapSelectMenu())


async def setup(bot):
    bot.add_command(map)
