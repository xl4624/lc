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
    # await bot.tree.sync()
    print(f"Logged in as {bot.user}")


@bot.event
async def load():
    for file in os.listdir("/home/rakib/lcleaderboard/lc-leaderboard-bot/cogs"):
        if file.endswith(".py"):
            await bot.load_extension(f"cogs.{file[:-3]}")


async def main():
    await load()

    ########################################
    # START BOT
    await bot.start(config.TOKEN)
    ########################################


asyncio.run(main())
