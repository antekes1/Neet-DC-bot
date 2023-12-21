import json
import os
import typing
import discord
from discord import app_commands, Interaction, Member, TextInput, permissions
from discord import Permissions
from discord.ext import commands
from discord.ui import Button, View
from utils.logging_on_server.logging_utils import sent_log

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

class MyView(View):
    def __init__(self, member, reason, rep_interaction, client: commands.Bot, log_interaction):
        super().__init__()
        self.user = member
        self.reason = reason
        self.interaction = rep_interaction
        self.client = client
        self.log_interaction = log_interaction

    #naprawić permisje i wiadomości
    async def ban_user(self, interaction):
        if self.user.guild_permissions.administrator:
            temp_embed = discord.Embed(colour=discord.Colour.red(), title="❌ Error",
                                       description="You can't ban an admin =((")
            # await self.interaction.response.send_message(embed=temp_embed, ephemeral=True)
            return False
        elif interaction.user.guild_permissions.administrator:
            channel = await self.user.create_dm()
            await self.user.ban(reason=self.reason)
            await channel.send(f"You have been baned on **{self.interaction.guild.name}** reason: {self.reason}")
            embed1 = discord.Embed(colour=discord.Colour.red(), title="Ban", description=f'Ban a {self.user.mention}')
            embed1.set_footer(text="Logs by Neet!")
            try:
                embed1.set_author(name=self.interaction.user.name, icon_url=self.interaction.user.avatar.url)
            except:
                embed1.set_author(name=self.interaction.user.name)
            embed1.add_field(name="reason", value=self.reason, inline=False)
            await sent_log(self, server=self.interaction.guild.id, message=embed1, interaction=self.interaction, client=self.client)
            return True
        else:
            temp_embed = discord.Embed(colour=discord.Colour.red(), title="❌ Error",
                                       description="You can't ban an admin =((")
            return False

    @discord.ui.button(label="Ban user", style=discord.ButtonStyle.danger, emoji="⛔", custom_id="ban_user_btn")
    async def button_callback(self, interaction: discord.Interaction, button: discord.Button):
        output = await self.ban_user(interaction=interaction)
        if output != False:
            button.disabled = True
            button.label = "Banned"
            button_1 = [x for x in self.children if x.custom_id=="ignore_btn"][0]
            button_1.disabled = True
            emb = interaction.message.embeds[0]
            await interaction.response.edit_message(embed=emb, view=self)

    @discord.ui.button(label="It's fine", style=discord.ButtonStyle.green, custom_id='ignore_btn')
    async def fine_button_callback(self, interaction: discord.Interaction, button: discord.Button):
        if interaction.user.guild_permissions.administrator:
            button.disabled = True
            button.label = "Oki !!!"
            button_1 = [x for x in self.children if x.custom_id == "ban_user_btn"][0]
            button_1.disabled = True
            emb = interaction.message.embeds[0]
            await interaction.response.edit_message(embed=emb, view=self)

async def sent_report(self, interaction: discord.Interaction, server, user, reason, message):
    this_interaction = Interaction
    channel_id = get_channel(self, server)
    if channel_id != None:
        channel = interaction.channel.guild.get_channel(channel_id)
        if message.author.id != interaction.client.user.id:
            embed = discord.Embed(colour=discord.Colour.dark_red(), title="Message report", description=f'User {user.name} reported a message form user {message.author.name}')
            try:
                embed.set_author(name=user.name, icon_url=user.avatar.url)
            except:
                embed.set_author(name=user.name)
            embed.add_field(name='Content: ', value='`' + message.content + '`')
            embed.add_field(name="Reason: ", value=reason, inline=False)
            embed.set_footer(text="Logs by Neet!")
            if message.embeds:
                embed.add_field(name='Embeds: ', value='￬ available down')
                #await channel.send(embed=embed)
            #### add buttons ####
            view = MyView(member=message.author, reason=reason, rep_interaction=interaction, client=commands.Bot, log_interaction=this_interaction)
            await channel.send(embed=embed, view=view)
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