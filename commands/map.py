import os
import random

import discord
from discord.ext import commands


class MapSelectMenu(discord.ui.Select):
    def __init__(self, game):
        self.game = game
        self.maps = [m[:-4] for m in os.listdir(f'./images/maps/{self.game}') if m.endswith('.png')]
        options = [discord.SelectOption(label=m) for m in self.maps]
        super().__init__(placeholder='除外するマップを選択…', min_values=0, max_values=len(options) - 1, options=options)

    async def callback(self, interaction: discord.Integration):
        pickedmap = random.choice([m for m in self.maps if m not in self.values])
        embed = discord.Embed(title=pickedmap, colour=discord.Colour.red())
        embed.set_image(url=f'attachment://{pickedmap}.png')
        embed.set_footer(text='BAN: ' + (' '.join(self.values) or 'なし'))
        attachments = [discord.File(f'./images/maps/{self.game}/{pickedmap}.png', filename=f'{pickedmap}.png')]
        await interaction.response.edit_message(embed=embed, attachments=attachments, view=None)


class MapSelectMenuView(discord.ui.View):
    def __init__(self, game):
        super().__init__()
        self.add_item(MapSelectMenu(game))


@commands.hybrid_command()
async def map(ctx):
    '''VALORANTのマップをランダムに選択'''
    await ctx.send(view=MapSelectMenuView('VALORANT'))


async def setup(bot):
    bot.add_command(map)
