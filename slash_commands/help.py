import typing

import discord
from discord import app_commands, Interaction, Member
from discord.ext import commands
from discord.app_commands import Choice, choices
from discord.ext.commands import Bot



class help(commands.Cog):

    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name='help', description="Help command")
    @app_commands.choices(command=[
        app_commands.Choice(name="ping", value="ping"),
    ])
    async def help(self, interaction: discord.Interaction, command: app_commands.Choice[str] = None):
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name="Help")
        if command != None:
            aaa = command.value
            for commandd in self.client.commands:
                print(commandd.name)
            descr = commands.Bot.commands
            print(descr)
        embed.add_field(name="Support server: ", value="https://discord.gg/mC2w6AaA")
        await interaction.response.send_message(embed=embed)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(help(client))