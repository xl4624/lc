import discord
import config
import os
import asyncio
from discord.ext import commands

########################################
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="lcl$", intents=intents)
########################################


# On Ready
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")


@bot.event
async def load():
    cogs_dir = os.path.join(os.path.dirname(__file__), "cogs")
    for file in os.listdir(cogs_dir):
        if file.endswith(".py"):
            await bot.load_extension(f"cogs.{file[:-3]}")
            print(f"loaded extension: cogs.{file[:-3]}")


async def main():
    await load()

    ########################################
    # START BOT
    await bot.start(config.TOKEN)
    ########################################


asyncio.run(main())
