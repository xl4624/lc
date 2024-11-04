import discord
from discord.ext import commands
from discord import app_commands
from lib.admins import getAdmins
import lib.dbfuncs as dbfuncs


class AdminRemove(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Admin Remove cog loaded")

    @app_commands.command(name="zremove", description="Remove a user (ADMIN ONLY)")
    @app_commands.describe(discord_user="discord user to remove")
    async def adminremove(self, interaction: discord.Interaction, discord_user: str):
        await interaction.response.defer()

        if interaction.user.id in getAdmins():
            if not dbfuncs.check_discord_user(discord_user):
                out = f"Discord user {discord_user} not registered"
                await interaction.followup.send(out)
                return

            dbfuncs.remove_user(discord_user)
            await interaction.followup.send(
                f"Removed {discord_user} from leaderboard and database."
            )

        else:
            await interaction.followup.send("You are not an admin")


async def setup(bot):
    await bot.add_cog(AdminRemove(bot))
