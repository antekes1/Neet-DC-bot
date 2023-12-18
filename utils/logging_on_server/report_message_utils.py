import json
import os
import typing
import discord
from discord import app_commands, Interaction, Member, TextInput, permissions
from discord import Permissions
from discord.ext import commands

def get_channel(self, server):
    server = str(server)
    serwers = []
    for file in os.listdir("servers/"):
        serwers.append(file)
    if server in serwers:
        file_path = "servers/" + server + '/config.json'
        with open(file_path, 'r') as config_file:
            info = json.load(config_file)
        if "rep_chat" in info:
            channel_id = info["rep_chat"]
            return channel_id
        else:
            return None
    else:
        return None

async def sent_report(self, interaction: discord.Interaction, server, user, reason, message):
    channel_id = get_channel(self, server)
    if channel_id != None:
        channel = interaction.channel.guild.get_channel(channel_id)
        if message.author.id != interaction.client.user.id:
            embed = discord.Embed(colour=discord.Colour.dark_red(), title="Message report", description=f'User {user.name} reported a message form user {message.author.name}')
            embed.set_author(name=user.name, icon_url=user.avatar.url)
            embed.add_field(name='Content: ', value='`' + message.content + '`')
            embed.add_field(name="Reason: ", value=reason, inline=False)
            embed.set_footer(text="Logs by Neet!")
            if message.embeds:
                embed.add_field(name='Embeds: ', value='￬ available down')
                #await channel.send(embed=embed)
            await channel.send(embed=embed)
            return [True]
        else:
            return [False, "You can't report bot message"]
    else:
        return [False, "This funtion is not available on your server"]

async def set_rep_channel(self, interaction: discord.Interaction, server, channel):
    server = str(server)
    serwers = []
    for file in os.listdir("servers/"):
        serwers.append(file)
    if server in serwers:
        file_path = "servers/" + server + '/config.json'
        data = {"rep_chat": channel}
        with open(file_path, 'r') as config_file:
            info = json.load(config_file)
        info["rep_chat"] = channel
        to_save = info
        with open(file_path, 'w') as config_file:
            json.dump(info, config_file)
        return ['updated', 'True']
    else:
        os.mkdir(f'servers/{server}')
        file_path = "servers/" + server + '/config.json'
        data = {"rep_chat": channel}
        with open(file_path, 'w') as config_file:
            json.dump(data, config_file)
        return ['created', 'True']

async def rep_status(self, interaction: discord.Interaction, server):
    server = str(server)
    serwers = []
    for file in os.listdir("servers/"):
        serwers.append(file)
    if server in serwers:
        file_path = "servers/" + server + '/config.json'
        with open(file_path, 'r') as config_file:
            info = json.load(config_file)
        if 'rep_chat' in info:
            return [True, info['rep_chat']]
        else:
            return [False]
    else:
        return [False]