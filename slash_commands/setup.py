import typing

import discord
from discord import app_commands, Interaction, Member, channel, TextChannel, permissions
from discord.ext import commands
from discord.app_commands import Choice, choices
from discord.ext.commands import Bot
from utils.logging_on_server.loggingg import set_logs_channel, sent_log, logs_status



class setupp(commands.Cog):

    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name='setup', description="Setup command")
    # @app_commands.choices(command=[
    #     app_commands.Choice(name="", value="ping"),
    # ])
    @app_commands.default_permissions(administrator=True)
    async def setupp(self, interaction: discord.Interaction, logs_channel: TextChannel = None):
        embed = discord.Embed(colour=discord.Colour.blue(), description="This is a setup command")
        embed.set_author(name="Setup")
        status = await logs_status(self, interaction, server=interaction.guild.id)
        if status == True:
            embed.add_field(name="Logs status", value="Logging is turned on", inline=False)
        else:
            embed.add_field(name="Logs status", value="Logging is not setup", inline=False)
        if logs_channel != None:
            status = await set_logs_channel(self, server=interaction.guild.id, channel=logs_channel.id, interaction=interaction)
            if status[0] == 'created' and status[1] == 'True':
                embed.add_field(name="Setup logs channel", value="Created succesfull", inline=False)

                embed1 = discord.Embed(colour=discord.Colour.green(), title="Setup logs", description=f'Logs setup succesfully =)')
                embed1.set_footer(text="Logs by Neet! discord bot")
                embed1.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)

                await sent_log(self, server=interaction.guild.id, message=embed1, interaction=interaction, client=self.client)
            else:
                embed.add_field(name="Setup logs channel", value="Failed", inline=False)
        embed.set_footer(text="Neet!")
        await interaction.response.send_message(embed=embed)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(setupp(client))