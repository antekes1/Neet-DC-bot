import json
import os
import typing
import discord
from discord import app_commands, Interaction, Member, TextInput, permissions
from discord import Permissions
from discord.ext import commands

def get_channell(self, server):
    server = str(server)
    serwers = []
    for file in os.listdir("servers/"):
        serwers.append(file)
    #błąd przy konwersji na str
    if server in serwers:
        file_path = "servers/" + server + '/config.json'
        with open(file_path, 'r') as config_file:
            info = json.load(config_file)
        channel_id = info["logs_chat"]
        return channel_id
    else:
        return None

async def sent_log(self, interaction: discord.Interaction, message, server, client):
    channel_id = get_channell(self, server)
    if channel_id != None:
        channel = interaction.channel.guild.get_channel(int(channel_id))
        await channel.send(embed=message)

async def set_logs_channel(self, interaction: discord.Interaction, server, channel):
    server = str(server)
    serwers = []
    for file in os.listdir("servers/"):
        serwers.append(file)
    if server in serwers:
        return ['updated', 'False']
    else:
        os.mkdir(f'servers/{server}')
        file_path = "servers/" + server + '/config.json'
        data = {"logs_chat": str(channel)}
        with open(file_path, 'w') as config_file:
            json.dump(data, config_file)
        return ['created', 'True']

async def logs_status(self, interaction: discord.Interaction, server):
    server = str(server)
    serwers = []
    for file in os.listdir("servers/"):
        serwers.append(file)
    if server in serwers:
        file_path = "servers/" + server + '/config.json'
        with open(file_path, 'r') as config_file:
            info = json.load(config_file)
        if 'logs_chat' in info:
            return True
        else:
            return False
    else:
        return False