import typing

import discord
from discord import app_commands, Interaction, Member
from discord.ext import commands
from discord.app_commands import Choice, choices
from discord.ext.commands import Bot

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
        await interaction.response.send_message(embed=embed)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(help(client))