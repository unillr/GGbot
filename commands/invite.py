import discord
from discord import app_commands


class InviteView(discord.ui.View):
    def __init__(self, embed: discord.Embed, user: discord.User | discord.Member):
        super().__init__(timeout=86400)
        self.embed = embed
        self.users = [user.mention]

    @discord.ui.button(style=discord.ButtonStyle.primary, label='参加')
    async def _join(self, interaction: discord.Interaction,
                    button: discord.ui.Button):
        self.users.append(interaction.user.mention)
        self.embed.set_field_at(0, name='参加者', value='\n'.join(self.users))
        await interaction.response.edit_message(embed=self.embed)

    @discord.ui.button(style=discord.ButtonStyle.danger, label='招集')
    async def join(self, interaction: discord.Interaction,
                   button: discord.ui.Button):
        if interaction.user.mention in self.users:
            await interaction.response.send_message(' '.join(self.users))
        else:
            await interaction.response.send_message('参加者以外は招集できないよ!', ephemeral=True)


@app_commands.command(name='bo')
async def invite(interaction: discord.Interaction, content: str):
    '''募集用コマンド'''
    embed = discord.Embed()
    embed.add_field(name='参加者', value=interaction.user.mention)
    await interaction.response.send_message(content=content, embed=embed,
                                            view=InviteView(embed, interaction.user))


async def setup(bot):
    bot.tree.add_command(invite)
