import typing
import discord
from discord import app_commands, Interaction, Member
from discord.ext import commands
from discord.app_commands import Choice, choices
from discord.ext.commands import Bot
from discord.ui import Select

class RepSelect(Select):
    def __init__(self, bot: commands.Bot, interaction):
        super().__init__(
            placeholder="Choose a category",
            options=[
                discord.SelectOption(
                   label="Setup functions", value='setup'
                ),
                discord.SelectOption(
                    label="Commands", value='commands'
                ),
            ],
            min_values=1,
            max_values=1,
        )

        self.bot = bot
        self.interacion_xD = interaction

    async def callback(self, interaction: discord.Interaction):
        option = self.values[0]
        emb = interaction.message.embeds[0]
        if option == "setup":
            embed = discord.Embed(colour=discord.Colour.blurple(), title="Setup command", description="How to use setup command ?")
            embed.set_author(name="Help")
            embed.add_field(name='Turning on logging', value="use /setup and logs channel options and set valid channel. ")
            embed.add_field(name="Support server: ", value="https://discord.gg/mC2w6AaA")
        elif option == "commands":
            embed = discord.Embed(colour=discord.Colour.blurple(), title="Commands:")
            embed.set_author(name="Help")
            embed.add_field(name="Support server: ", value="https://discord.gg/mC2w6AaA")
        await interaction.response.edit_message(embed=embed)


class DropdownView(discord.ui.View):
    def __init__(self, dropdown: discord.ui.Select):
        super().__init__()
        self.add_item(dropdown)


class help(commands.Cog):

    def __init__(self, client: commands.Bot):
        self.client = client
        self.bot = commands.Bot

    @app_commands.command(name='help', description="Help command")
    # @app_commands.choices(command=[
    #     app_commands.Choice(name="ping", value="ping"),
    # ])
    async def help(self, interaction: discord.Interaction):
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name="Help")
        # for command in self.bot.walk_commands()
        #     if isinstance(command, commands.Command):
        #         embed.add_field(name=command.name, value=command.help, inline=False)
        embed.add_field(name="Support server: ", value="https://discord.gg/mC2w6AaA")
        dropdown = RepSelect(bot=commands.Bot, interaction=interaction)
        view = DropdownView(dropdown)
        await interaction.response.send_message(embed=embed, view=view)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(help(client))