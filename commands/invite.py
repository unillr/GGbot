import discord
from discord import app_commands


class InviteView(discord.ui.View):
    def __init__(self, user: str, number: int | None):
        super().__init__(timeout=86400)
        self.number = number
        self.participants = [user]
        self.waitings = []
        self.canceled = []
        self.members = {'参加者': self.participants, '空き待ち': self.waitings, 'キャンセル': self.canceled}

    @discord.ui.button(style=discord.ButtonStyle.primary, label='参加')
    async def _join(self, interaction: discord.Interaction,
                    button: discord.ui.Button):
        new_user = interaction.user.mention
        if new_user in self.participants or new_user in self.waitings:
            await interaction.response.send_message('すでに参加しているよ!', ephemeral=True)
            return
        if self.number is None or len(self.participants) - 1 < self.number:
            self.participants.append(new_user)
        else:
            self.waitings.append(new_user)
        if new_user in self.canceled:
            self.canceled.remove(new_user)

        embed = discord.Embed(title=f'残り募集人数: {self.number - len(self.participants) + 1}'
                              if self.number is not None else None)
        for n, v in self.members.items():
            embed.add_field(name=n, value='\n'.join(v) if v else 'なし')
        await interaction.response.edit_message(embed=embed)

    @discord.ui.button(style=discord.ButtonStyle.secondary, label='キャンセル')
    async def cancel(self, interaction: discord.Interaction,
                     button: discord.ui.Button):
        cancel_user = interaction.user.mention
        if cancel_user in self.participants:
            self.participants.remove(cancel_user)
            self.canceled.append(cancel_user)
            if self.waitings:
                new_participant = self.waitings.pop(0)
                self.participants.append(new_participant)
        elif cancel_user in self.waitings:
            self.waitings.remove(cancel_user)
            self.canceled.append(cancel_user)
        else:
            await interaction.response.send_message('まだ参加していないよ!', ephemeral=True)
            return

        embed = discord.Embed(title=f'残り募集人数: {self.number - len(self.participants) + 1}'
                              if self.number is not None else None)
        for n, v in self.members.items():
            embed.add_field(name=n, value='\n'.join(v) if v else 'なし')
        await interaction.response.edit_message(embed=embed)

    @discord.ui.button(style=discord.ButtonStyle.danger, label='招集')
    async def calling(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.mention not in self.participants:
            await interaction.response.send_message('参加者以外は招集できないよ!', ephemeral=True)
            return
        await interaction.response.send_message(' '.join(self.participants))


@app_commands.command(name='bo')
@app_commands.describe(content='募集内容', number='募集人数(自分を除く)')
async def invite(interaction: discord.Interaction, content: str, number: int | None):
    '''募集用コマンド'''
    if number is not None:
        content = f'{content} @{number}'
    embed = discord.Embed(title=f'残り募集人数: {number}' if number is not None else None)
    embed.add_field(name='参加者', value=interaction.user.mention)
    embed.add_field(name='空き待ち', value='なし')
    embed.add_field(name='キャンセル', value='なし')
    await interaction.response.send_message(content=content,
                                            embed=embed,
                                            view=InviteView(interaction.user.mention, number))


async def setup(bot):
    bot.tree.add_command(invite)
