import os
import random

import discord
from discord.ext import commands


MAPIMAGES_DIR = 'images/maps'


class GameSelectButton(discord.ui.View):
    @discord.ui.button(label='VALORANT', style=discord.ButtonStyle.red)
    async def map_valorant(self, interaction: discord.Integration, button: discord.ui.Button):
        mapimages = list(filter(lambda file: file.endswith('.png'), os.listdir(f'./{MAPIMAGES_DIR}/VALORANT')))
        mapimage = random.choice(mapimages)
        embed = discord.Embed(title=mapimage.removesuffix('.png').upper(), colour=discord.Colour.red())
        embed.set_image(url=f'attachment://{mapimage}')
        attachment = discord.File(f'./{MAPIMAGES_DIR}/VALORANT/{mapimage}', filename=mapimage)
        await interaction.response.edit_message(embed=embed, attachments=[attachment])

    @discord.ui.button(label='Splatoon', style=discord.ButtonStyle.grey, disabled=True)
    async def map_splatoon(self, interaction: discord.Integration, button: discord.ui.Button):
        pass


@commands.hybrid_command()
async def map(ctx):
    '''ランダムにマップを返す'''
    embed = discord.Embed(title='ゲームを選択', colour=discord.Colour.blurple())
    await ctx.send(embed=embed, view=GameSelectButton())

async def setup(bot):
    bot.add_command(map)

