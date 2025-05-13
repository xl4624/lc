import discord
import config
import os
import asyncio
from discord.ext import commands
from pathlib import Path

########################################
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="lcl$", intents=intents)
########################################


# On Ready
@bot.event
async def on_ready():
    # await bot.tree.sync()
    print(f"Logged in as {bot.user}")


@bot.event
async def load():
    for file in Path(__file__).parent.glob("cogs/*.py"):
        await bot.load_extension(f"cogs.{file.name[:-3]}")


async def main():
    await load()

    ########################################
    # START BOT
    await bot.start(config.TOKEN)
    ########################################


asyncio.run(main())
