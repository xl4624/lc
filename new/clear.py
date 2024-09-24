import typing
import discord
from discord.ext import commands
from discord import app_commands
from lib.admins import ADMINS
import lib.dbfuncs as dbfuncs


class ClearPoints(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Clear Points cog loaded")

    @app_commands.command(
        name="zclear", description="Clear EVERYONE's points AND wins (ADMIN ONLY)"
    )
    @app_commands.describe(confirm="Type 'CONFIRM' to clear all points")
    async def clearpoints(
        self, interaction: discord.Interaction, confirm: typing.Optional[str]
    ):
        await interaction.response.defer()
        if interaction.user.id in ADMINS:
            if confirm == "CONFIRM":
                dbfuncs.CLEAR_ALL_POINTS()
                await interaction.followup.send("Cleared all points")
            else:
                await interaction.followup.send("Points not cleared, no confirmation")

        else:
            await interaction.followup.send("You are not an admin")


async def setup(bot):
    await bot.add_cog(ClearPoints(bot))
