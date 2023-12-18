import discord
from discord import app_commands, Interaction, Member
from discord.ext import commands

class ping(commands.Cog):

    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name='ping', description="This is the ping command")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'pong {interaction.user.mention}')

async def setup(client: commands.Bot) -> None:
    await client.add_cog(ping(client))