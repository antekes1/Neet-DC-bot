from typing import Any

import discord
from discord import app_commands, Interaction, Member, SelectMenu
from discord._types import ClientT
from discord.ui import Select
from discord.ext import commands
from discord.ext.commands import bot
from utils.logging_on_server.report_message_utils import sent_report

class RepSelect(Select):
    def __init__(self, bot: commands.Bot, message, user, interaction):
        super().__init__(
            placeholder="Choose a reason",
            options=[
                discord.SelectOption(
                   label="vulgarity or offensive message", value='vulgarity or offensive message'
                ),
                discord.SelectOption(
                    label="mass ping", value='mass ping'
                ),
            ]
        )

        self.bot = bot
        self.message = message
        self.user = user
        self.interaction = interaction

    async def callback(self, interaction: discord.Interaction):
        info = await sent_report(self, server=interaction.guild.id, user=self.user, message=self.message,
                                 reason=self.values[0], interaction=interaction)
        if info[0] == True:
            embed = discord.Embed(colour=discord.Colour.green(), title="Success", description="Message reported")
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(colour=discord.Colour.red(), title="Error", description=info[1])
            await interaction.response.send_message(embed=embed, ephemeral=True)

class DropdownView(discord.ui.View):
    def __init__(self, dropdown: discord.ui.Select):
        super().__init__(timeout=60)
        self.add_item(dropdown)

class reporting_message(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.ctx_menu = app_commands.ContextMenu(
            name='Report message',
            callback=self.report_message,
        )
        self.bot.tree.add_command(self.ctx_menu)

    async def report_message(self, interaction: discord.Interaction, message: discord.Message):
        dropdown = RepSelect(message=message, user=interaction.user, interaction=interaction, bot=commands.Bot)
        view = DropdownView(dropdown)
        await interaction.response.send_message("Select a reason", view=view, ephemeral=True)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(reporting_message(client))