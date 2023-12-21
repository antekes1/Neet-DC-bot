import typing
import sys
import discord
from discord import app_commands, Interaction, Member, TextInput, permissions
from discord import Permissions
from discord.ext import commands
from utils.logging_on_server.logging_utils import sent_log

class ban(commands.Cog):

    def __init__(self, client: commands.Bot):
        self.client = client

    #naprawić permisje tak aby nie wywalało missing permission
    async def ban_user(self, interaction, user, reason):

        if user.guild_permissions.administrator:
            temp_embed = discord.Embed(colour=discord.Colour.red(), title="❌ Error",
                                       description="You can't ban an admin =((")
            await interaction.response.send_message(embed=temp_embed)
        elif user.id == interaction.user.id:
            temp_embed = discord.Embed(colour=discord.Colour.red(), title="❌ Error",
                                       description="You can't ban yourself")
            await interaction.response.send_message(embed=temp_embed)
        elif not interaction.user.guild_permissions.administrator:
            temp_embed = discord.Embed(colour=discord.Colour.red(), title="❌ Error",
                                       description="You can't ban bacause you are not an admin =((")
            await interaction.response.send_message(embed=temp_embed)
        else:
            if reason == None:
                reason = "no reason"
            channel = await user.create_dm()
            await channel.send(f"You have been baned on **{interaction.guild.name}** reason: {reason}")
            await user.ban(reason=reason)
            await interaction.response.send_message(f'✅ Banned user {user.mention} for {reason}')
            embed1 = discord.Embed(colour=discord.Colour.red(), title="Ban", description=f'Ban a {user.mention}')
            embed1.set_footer(text="Logs by Neet!")
            embed1.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)
            embed1.add_field(name="reason", value=reason, inline=False)
            await sent_log(self, server=interaction.guild.id, message=embed1, interaction=interaction, client=self.client)

    @app_commands.command(name='ban', description="Ban a user")
    @app_commands.default_permissions(ban_members=True)
    #defoult perm
    async def ban(self, interaction: discord.Interaction,
                  user: Member, reason: str = None):
        await self.ban_user(interaction, user, reason)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(ban(client))