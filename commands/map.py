import json
import random

import discord
from discord import app_commands
from discord.ext import commands


class GameSelectButton(discord.ui.Button[discord.ui.View]):
    def __init__(self, game: str) -> None:
        self.game: str = game
        super().__init__(label=self.game, style=discord.ButtonStyle.primary)

    async def callback(self, interaction: discord.Interaction) -> None:
        await interaction.response.edit_message(view=MapSelectMenuView(self.game))


class MapSelectMenu(discord.ui.Select[discord.ui.View]):
    def __init__(self, game: str) -> None:
        self.game: str = game
        with open('./images/maps/maps.json', 'r', encoding='utf-8') as f:
            self.maps: dict[str, str] = json.load(f)[self.game]
        options: list[discord.SelectOption] = [
            discord.SelectOption(label=m) for m in self.maps.keys()
            ]
        super().__init__(placeholder='除外するマップを選択…',
                         min_values=0,
                         max_values=len(options) - 1,
                         options=options)

    async def callback(self, interaction: discord.Interaction) -> None:
        map_candicates: list[str] = [m for m in self.maps.keys() if m not in self.values]
        map_name: str = random.choice(map_candicates)
        map_image: str = self.maps[map_name]
        embed: discord.Embed = discord.Embed(title=map_name, colour=discord.Colour.red())
        embed.set_image(url=f'attachment://{map_image}')
        embed.set_footer(text='BAN: ' + (' / '.join(self.values) or 'なし'))
        attachments: list[discord.File] = [
            discord.File(f'./images/maps/{self.game}/{map_image}', filename=map_image)
            ]
        await interaction.response.edit_message(embed=embed, attachments=attachments, view=None)


class MapSelectMenuView(discord.ui.View):
    def __init__(self, selected_game: str = 'VALORANT') -> None:
        super().__init__()
        with open('./images/maps/maps.json', 'r', encoding='utf-8') as f:
            games: list[str] = json.load(f).keys()
        for game in games:
            self.add_item(GameSelectButton(game))
        self.add_item(MapSelectMenu(selected_game))


@app_commands.command(name='map')
async def random_map(interaction: discord.Interaction) -> None:
    '''マップをランダムに選択'''
    await interaction.response.send_message(view=MapSelectMenuView())


async def setup(bot: commands.Bot) -> None:
    bot.tree.add_command(random_map)
