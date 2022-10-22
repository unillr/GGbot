import discord
from discord import app_commands


class InviteView(discord.ui.View):
    def __init__(self, embed: discord.Embed, user: str, number: int | None):
        super().__init__(timeout=86400)
        self.embed = embed
        self.number = number
        self.participants = [user]
        self.inqueue = []
        self.canceled = []

    @discord.ui.button(style=discord.ButtonStyle.primary, label='参加')
    async def _join(self, interaction: discord.Interaction,
                    button: discord.ui.Button):
        new_user = interaction.user.mention
        if new_user in self.canceled:
            self.canceled.remove(new_user)
        elif new_user in self.participants or new_user in self.inqueue:
            await interaction.response.send_message('すでに参加しているよ!', ephemeral=True)
            return
        if self.number is None or len(self.participants) - 1 < self.number:
            self.participants.append(new_user)
        else:
            self.inqueue.append(new_user)

        self.embed.set_field_at(0, name='参加者',
                                value='\n'.join(self.participants) if self.participants else 'なし')
        self.embed.set_field_at(1, name='空き待ち',
                                value='\n'.join(self.inqueue) if self.inqueue else 'なし')
        self.embed.set_field_at(2, name='キャンセル',
                                value='\n'.join(self.canceled) if self.canceled else 'なし')
        await interaction.response.edit_message(embed=self.embed)

    @discord.ui.button(style=discord.ButtonStyle.secondary, label='キャンセル')
    async def cancel(self, interaction: discord.Interaction,
                     button: discord.ui.Button):
        new_user = interaction.user.mention
        if new_user in self.participants:
            self.participants.remove(new_user)
            self.canceled.append(new_user)
            if self.inqueue:
                new_participant = self.inqueue.pop(0)
                self.participants.append(new_participant)
        elif new_user in self.inqueue:
            self.inqueue.remove(new_user)
            self.canceled.append(new_user)
        else:
            await interaction.response.send_message('まだ参加していないよ!', ephemeral=True)
            return

        self.embed.set_field_at(0, name='参加者',
                                value='\n'.join(self.participants) if self.participants else 'なし')
        self.embed.set_field_at(1, name='空き待ち',
                                value='\n'.join(self.inqueue) if self.inqueue else 'なし')
        self.embed.set_field_at(2, name='キャンセル',
                                value='\n'.join(self.canceled) if self.canceled else 'なし')
        await interaction.response.edit_message(embed=self.embed)

    @discord.ui.button(style=discord.ButtonStyle.danger, label='招集')
    async def join(self, interaction: discord.Interaction,
                   button: discord.ui.Button):
        if interaction.user.mention in self.participants:
            await interaction.response.send_message(' '.join(self.participants))
        else:
            await interaction.response.send_message('参加者以外は招集できないよ!', ephemeral=True)


@app_commands.command(name='bo')
@app_commands.describe(content='募集内容', number='参加人数(自分を除く)')
async def invite(interaction: discord.Interaction, content: str, number: int | None):
    '''募集用コマンド'''
    content = f'{content} @{number}' if number is not None else content
    embed = discord.Embed()
    embed.add_field(name='参加者', value=interaction.user.mention)
    embed.add_field(name='空き待ち', value='なし')
    embed.add_field(name='キャンセル', value='なし')
    await interaction.response.send_message(content=content,
                                            embed=embed,
                                            view=InviteView(
                                                embed,
                                                interaction.user.mention,
                                                number
                                                ))


async def setup(bot):
    bot.tree.add_command(invite)
