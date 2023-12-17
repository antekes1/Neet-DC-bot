import discord
from discord import app_commands, Interaction, Member
from discord.ext import commands
from discord.ext.commands import bot


class get_user_info(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.ctx_menu = app_commands.ContextMenu(
            name='Show user info',
            callback=self.get_user_info, # set the callback of the context menu to "my_cool_context_menu"
        )
        self.bot.tree.add_command(self.ctx_menu) # add the context menu to the tree

    async def get_user_info(self, interaction: discord.Interaction, member: discord.Member):
        embed = discord.Embed(colour=discord.Colour.dark_blue())
        embed.set_author(name=member.name)
        embed.set_thumbnail(url=member.avatar)
        embed.add_field(name="Join date: ", value=member.joined_at.date(), inline=False)
        # embed.add_field(name="At: ", value=member.joined_at.hour, inline=False)
        done = ""
        for i in range(len(member.roles)):
            done = done + str(member.roles[i]) + ', '
        embed.add_field(name="Role:", value=done)
        await interaction.response.send_message(embed=embed)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(get_user_info(client))