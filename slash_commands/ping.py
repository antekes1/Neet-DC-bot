import discord
from discord import app_commands, Interaction, Member
from discord.ext import commands
from discord.ui import Button, View

class ping(commands.Cog):

    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name='ping', description="This is the ping command")
    async def ping(self, interaction: discord.Interaction):
        embed1 = discord.Embed(colour=discord.Colour.blue())
        embed1.add_field(name="Pong", value=interaction.user.mention, inline=False)
        button = Button(label="Ping again", style=discord.ButtonStyle.green)

        async def button_callback(interaction):
            await interaction.response.send_message("Pong!!!", ephemeral=True)

        button.callback = button_callback
        view = View()
        view.add_item(button)
        await interaction.response.send_message(embed=embed1, view=view)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(ping(client))