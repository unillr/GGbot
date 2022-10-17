import discord
from discord import app_commands
from discord.ext import commands


@app_commands.context_menu(name='VCから切断')
async def kick_from_voice_channel(interaction: discord.Interaction,
                                  member: discord.Member) -> None:
    await member.move_to(None)
    await interaction.response.send_message(f'{member.mention}をVCから切断したよ!', ephemeral=True)
    await member.send(f'{interaction.user}によってVCから切断されました')


async def setup(bot: commands.Bot) -> None:
    bot.tree.add_command(kick_from_voice_channel)
