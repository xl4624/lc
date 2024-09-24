import typing
import discord
from discord.ext import commands
from discord import app_commands
from lib.admins import ADMINS
import lib.dbfuncs as dbfuncs


class AdminReset(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Admin Points cog loaded")

    @app_commands.command(
        name="zreset", description="Reset the leaderboard (ADMIN ONLY)"
    )
    @app_commands.describe(interval="Choose a reset interval")
    @app_commands.describe(confirmation="type CONFIRM to confirm a RESET")
    @app_commands.choices(
        interval=[
            app_commands.Choice(name="Weekly", value="7"),
            app_commands.Choice(name="Biweekly", value="14"),
            app_commands.Choice(name="Monthly", value="30"),
        ]
    )
    async def AdminReset(
        self,
        interaction: discord.Interaction,
        confirmation: typing.Optional[str],
        interval: typing.Optional[app_commands.Choice[str]],
    ):
        await interaction.response.defer()
        if interaction.user.id in ADMINS:
            if confirmation != "CONFIRM":
                await interaction.followup.send(
                    "Please type CONFIRM to confirm a RESET"
                )
                return
            dbfuncs.CLEAR_ALL_POINTS(int(interval.value) if interval else None)
            await interaction.followup.send(
                f"Leaderboard has been reset for the interval of {interval} days"
            )

        else:
            await interaction.followup.send("You are not an admin")


async def setup(bot):
    await bot.add_cog(AdminReset(bot))
