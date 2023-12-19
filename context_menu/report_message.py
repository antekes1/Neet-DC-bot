import discord
from discord import app_commands, Interaction, Member
from discord.ext import commands
from discord.ext.commands import bot
from utils.logging_on_server.report_message_utils import sent_report

class reporting_message(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.ctx_menu = app_commands.ContextMenu(
            name='Report message',
            callback=self.report_message,
        )
        self.bot.tree.add_command(self.ctx_menu)

    async def report_message(self, interaction: discord.Interaction, message: discord.Message):
        info = await sent_report(self, server=interaction.guild.id, user=interaction.user, message=message, reason="not supported now", interaction=interaction)
        if info[0] == True:
            embed = discord.Embed(colour=discord.Colour.green(), title="Success", description="Message reported")
            await interaction.response.send_message(embed)
        else:
            embed = discord.Embed(colour=discord.Colour.red(), title="Error", description=info[1])
            await interaction.response.send_message(embed=embed)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(reporting_message(client))