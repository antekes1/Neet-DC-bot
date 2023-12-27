import discord
from discord import app_commands, Interaction, Member
from discord._types import ClientT
from discord.ext import commands
from discord.ext.commands import bot
from discord.ui import Modal
from utils.logging_on_server.logging_utils import sent_log, logs_status

class ReportModal(Modal, title="Report user"):

    def __init__(self, member):
        super().__init__()
        self.member = member

    user_name = discord.ui.TextInput(label="Enter your user name", placeholder="eg. daniel", required=True, style=discord.TextStyle.short)
    reason = discord.ui.TextInput(label="Reason", placeholder="why?", required=True, style=discord.TextStyle.paragraph)


    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'Thanks for report, {self.member.name} for {self.reason}', ephemeral=True)
        embed1 = discord.Embed(colour=discord.Colour.red(), title="Report user form", description=f'Report {self.member.name} by {interaction.user.name}')
        embed1.set_footer(text="Logs by Neet!")
        embed1.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)
        embed1.add_field(name="reason: ", value=self.reason, inline=False)
        embed1.add_field(name="reported user id: ", value=self.member.id, inline=False)
        client = commands.Bot
        await sent_log(self, server=interaction.guild.id, message=embed1, interaction=interaction, client=client)

class rep_user(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.ctx_menu = app_commands.ContextMenu(
            name='Report user',
            callback=self.report_user, # set the callback of the context menu to "my_cool_context_menu"
        )
        self.bot.tree.add_command(self.ctx_menu) # add the context menu to the tree

    async def report_user(self, interaction: discord.Interaction, member: discord.Member):
        status = await logs_status(interaction=interaction, server=interaction.guild.id, self=self)
        if status[0] == True:
            await interaction.response.send_modal(ReportModal(member))
        else:
            await interaction.response.send_message("This option isn't available. Help for setting this up in help command", ephemeral=True)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(rep_user(client))