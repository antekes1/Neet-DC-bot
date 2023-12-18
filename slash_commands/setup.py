import typing

import discord
from discord import app_commands, Interaction, Member, channel, TextChannel, permissions
from discord.ext import commands
from discord.app_commands import Choice, choices
from discord.ext.commands import Bot
from utils.logging_on_server.logging_utils import set_logs_channel, sent_log, logs_status
from utils.logging_on_server.report_message_utils import set_rep_channel, rep_status



class setupp(commands.Cog):

    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name='setup', description="Setup command")
    # @app_commands.choices(command=[
    #     app_commands.Choice(name="", value="ping"),
    # ])
    @app_commands.default_permissions(administrator=True)
    async def setupp(self, interaction: discord.Interaction, logs_channel: TextChannel = None, report_messages_logs_channel: TextChannel = None):
        embed = discord.Embed(colour=discord.Colour.blue(), description="This is a setup command")
        embed.set_author(name="Setup")

        if logs_channel != None:
            status = await set_logs_channel(self, server=interaction.guild.id, channel=logs_channel.id, interaction=interaction)
            if status[1] == 'True':
                embed.add_field(name="Setting up logs", value=f"{status[0]} successful", inline=False)

                embed1 = discord.Embed(colour=discord.Colour.green(), title="Logging setup", description=f'Logs setup succesfully =)')
                embed1.set_footer(text="Logs by Neet!")
                embed1.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)

                await sent_log(self, server=interaction.guild.id, message=embed1, interaction=interaction, client=self.client)
            else:
                embed.add_field(name="Setting up logs", value="Failed", inline=False)
        ####
        if report_messages_logs_channel != None:
            status = await set_rep_channel(self, server=interaction.guild.id, channel=report_messages_logs_channel.id, interaction=interaction)
            if status[1] == 'True':
                embed.add_field(name="Setting up reporting logs channel", value=f"{status[0]} successful", inline=False)

                embed1 = discord.Embed(colour=discord.Colour.green(), title="Report messages setup", description=f'Report messages logs setup succesfully =)')
                embed1.set_footer(text="Logs by Neet!")
                embed1.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)
                await sent_log(self, server=interaction.guild.id, message=embed1, interaction=interaction, client=self.client)
            else:
                embed.add_field(name="Setting up report messages logs", value="Failed", inline=False)
        ####
        status = await logs_status(self, interaction, server=interaction.guild.id)
        if status[0] == True:
            embed.add_field(name="Logs status", value=f"Logs are turned on, active on {status[1]} channel", inline=False)
        else:
            embed.add_field(name="Logs status", value="Logs are not setup", inline=False)
        embed.set_footer(text="Neet!")
        ####
        status = await rep_status(self, interaction, server=interaction.guild.id)
        if status[0] == True:
            embed.add_field(name="Logs status", value=f"Reporting message is turned on, active on {status[1]} channel", inline=False)
        else:
            embed.add_field(name="Logs status", value="Reporting message is not setup", inline=False)
        ####
        embed.set_footer(text="Neet!")
        await interaction.response.send_message(embed=embed)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(setupp(client))