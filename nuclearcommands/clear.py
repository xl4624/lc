import typing
import discord
from discord.ext import commands
from discord import app_commands
from lib.admins import getAdmins
import lib.dbfuncs as dbfuncs


class Adminclear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Admin Points cog loaded")

    @app_commands.command(
        name="zclear",
        description="clear the ENTIRE leaderboard (points and wins) (ADMIN ONLY)",
    )
    @app_commands.describe(confirmation="type CONFIRM to confirm a clear")
    async def Adminclear(
        self,
        interaction: discord.Interaction,
        confirmation: typing.Optional[str],
    ):
        await interaction.response.defer()
        if interaction.user.id in getAdmins():
            if confirmation != "CONFIRM":
                await interaction.followup.send("No confirmation, clear cancelled")
                return
            else:
                dbfuncs.CLEAR_ALL_POINTS(wins=True)
                await interaction.followup.send("Leaderboard has been cleared")

        else:
            await interaction.followup.send("You are not an admin")


async def setup(bot):
    await bot.add_cog(Adminclear(bot))
