import json
import random

import discord
from discord.ext import commands


class GameSelectButton(discord.ui.Button):
    def __init__(self, game):
        self.game = game
        super().__init__(label=self.game, style=discord.ButtonStyle.primary)
    
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.edit_message(view=MapSelectMenuView(self.game))


class MapSelectMenu(discord.ui.Select):
    def __init__(self, game):
        self.game = game
        with open(f'./images/maps/map.json', 'r', encoding='utf-8') as f:
            self.maps = json.load(f)[self.game]
        options = [discord.SelectOption(label=m) for m in self.maps.keys()]
        super().__init__(placeholder='除外するマップを選択…', min_values=0, max_values=len(options) - 1, options=options)

    async def callback(self, interaction: discord.Integration):
        map_candicates = [m for m in self.maps.keys() if m not in self.values]
        map_name = random.choice(map_candicates)
        map_image = self.maps[map_name]
        embed = discord.Embed(title=map_name, colour=discord.Colour.red())
        embed.set_image(url=f'attachment://{map_image}')
        embed.set_footer(text='BAN: ' + (' / '.join(self.values) or 'なし'))
        attachments = [discord.File(f'./images/maps/{self.game}/{map_image}', filename=map_image)]
        await interaction.response.edit_message(embed=embed, attachments=attachments, view=None)


class MapSelectMenuView(discord.ui.View):
    def __init__(self, selected_game='VALORANT'):
        super().__init__()
        with open('./images/maps/map.json', 'r', encoding='utf-8') as f:
            games = json.load(f).keys()
        for game in games:
            self.add_item(GameSelectButton(game))
        self.add_item(MapSelectMenu(selected_game))


@commands.hybrid_command(name='map')
async def random_map(ctx):
    '''マップをランダムに選択'''
    await ctx.send(view=MapSelectMenuView())


async def setup(bot):
    bot.add_command(random_map)
