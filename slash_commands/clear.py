import discord
from discord import app_commands, Interaction, Member
from discord.ext import commands
from discord.ui import Button, View

class clear(commands.Cog):

    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name='clear', description="This command clearing messages")
    @app_commands.default_permissions(manage_messages=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def clear(self, interaction: discord.Interaction, count: int = None):
        if count == None:
            info = "all"
        else:
            info = int(count)
        embed1 = discord.Embed(colour=discord.Colour.blue(), title=f"Clear {info}", description="Clearing ...")
        await interaction.response.send_message(embed=embed1, ephemeral=True)
        if count != None:
            z = await interaction.channel.purge(limit=count)
        else:
            z = await interaction.channel.purge(limit=1000000000000)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(clear(client))