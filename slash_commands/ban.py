import typing
import sys
import discord
from discord import app_commands, Interaction, Member, TextInput, permissions
from discord import Permissions
from discord.ext import commands
from utils.logging_on_server.logging import sent_log, get_channel
class ban(commands.Cog):

    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name='ban', description="Ban a user")
    @app_commands.default_permissions(ban_members=True)
    #defoult perm
    async def ban(self, interaction: discord.Interaction,
                  user: Member, reason: str = None):
        if user.guild_permissions.administrator:
            await interaction.response.send_message("You can't ban an admin =((")
        elif user.id == interaction.user.id:
            await interaction.response.send_message("You can't ban yourself")
        elif not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You can't ban bacause you are not an admin =((")
        else:
            if reason == None:
                reason = "no reason"
            channel = await user.create_dm()
            await channel.send(f"You have been baned on **{interaction.guild.name}** reason: {reason}")
            await user.ban(reason=reason)
            await interaction.response.send_message(f'Banned user {user.mention} for {reason}')
            embed1 = discord.Embed(colour=discord.Colour.red(), title="Ban", description=f'Banned {user.mention}')
            embed1.set_footer(text="Logs by Neet!")
            embed1.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)
            embed1.add_field(name="reason", value=reason, inline=False)
            await sent_log(self, server=interaction.guild.id, message=embed1, interaction=interaction, client=self.client)


async def setup(client: commands.Bot) -> None:
    await client.add_cog(ban(client))
