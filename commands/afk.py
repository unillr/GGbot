import os

import discord
from discord import app_commands
from discord.ext import commands


class MemberSelectMenu(discord.ui.Select):
    def __init__(self, members):
        options = [discord.SelectOption(label=m.display_name, value=str(m.id), description=str(m)) for m in members]
        super().__init__(placeholder='移動させる人を選択…', options=options)

    async def callback(self, interaction: discord.Interaction):
        member = interaction.guild.get_member(int(self.values[0]))
        await member.move_to(interaction.guild.afk_channel)
        await interaction.response.edit_message(content=f'{member.display_name}をAFKチャンネルに移動させたよ!', view=None)


class MemberSelectMenuView(discord.ui.View):
    def __init__(self, members):
        super().__init__()
        self.add_item(MemberSelectMenu(members))


@commands.hybrid_command()
@app_commands.describe(move_from='移動元のチャンネル')
async def afk(ctx, move_from: discord.VoiceChannel):
    '''指定した人をAFKチャンネルに移動'''
    if not move_from.members:
        await ctx.send('そのチャンネルには誰もいないよ!', ephemeral=True)
    elif ctx.author not in move_from.members:
        await ctx.send('自分のいるチャンネルを入力してね!', ephemeral=True)
    else:
        await ctx.send(view=MemberSelectMenuView(move_from.members))
    

async def setup(bot):
    bot.add_command(afk)
