import os
import discord
from discord.ext import commands
from discord import app_commands
import settings


def run():
    intents = discord.Intents.all()

    bot = commands.Bot(command_prefix='!', intents=intents)

    initial_extentions = []

    for filename in os.listdir('./slash_commands'):
        if filename.endswith('.py'):
            initial_extentions.append("slash_commands." + filename[:-3])

    for filename in os.listdir('./context_menu'):
        if filename.endswith('.py'):
            initial_extentions.append("context_menu." + filename[:-3])

    @bot.event
    async def on_ready():
        # await bot.load_extension("slash_commands.ping")
        # load commands
        print("==Slash commands: ==")
        for extention in initial_extentions:
            await bot.load_extension(extention)
            print(extention)
        synced = await bot.tree.sync()

        # info
        print('------------------------------')
        print("The bot is ready to use!!!")
        print(bot.user)
        print(f'Bot by {bot.application.owner}')
        print(f'Loaded commands: {str(len(synced))}')
        print('------------------------------')

        # activity
        await bot.change_presence(activity=discord.Game(name='life'))
        bot.remove_command("help")

    bot.run((settings.Bot_token))


if __name__ == "__main__":
    run()
