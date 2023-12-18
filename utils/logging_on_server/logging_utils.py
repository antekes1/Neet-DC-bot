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
        if "logs_chat" in info:
            channel_id = info["logs_chat"]
            return channel_id
        else:
            return None
    else:
        return None

async def sent_log(self, interaction: discord.Interaction, message, server, client):
    channel_id = get_channel(self, server)
    if channel_id != None:
        channel_id = int(channel_id)
        channel = interaction.channel.guild.get_channel(channel_id)
        await channel.send(embed=message)

async def set_logs_channel(self, interaction: discord.Interaction, server, channel):
    server = str(server)
    serwers = []
    for file in os.listdir("servers/"):
        serwers.append(file)
    if server in serwers:
        file_path = "servers/" + server + '/config.json'
        data = {"logs_chat": channel}
        with open(file_path, 'r') as config_file:
            info = json.load(config_file)
        info["logs_chat"] = channel
        to_save = info
        with open(file_path, 'w') as config_file:
            json.dump(info, config_file)
        return ['updated', 'True']
    else:
        os.mkdir(f'servers/{server}')
        file_path = "servers/" + server + '/config.json'
        data = {"logs_chat": channel}
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
            return [True, info['logs_chat']]
        else:
            return [False]
    else:
        return [False]