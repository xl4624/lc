import discord
from discord.ext import commands
from discord import app_commands
from lib.admins import ADMINS
import lib.dbfuncs as dbfuncs


class AdminRegister(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Admin Register cog loaded")

    @app_commands.command(name="zregister", description="Register a user (ADMIN ONLY)")
    @app_commands.describe(discord_user="discord user to register")
    @app_commands.describe(leetcode_user="leetcode user to register")
    async def adminregister(
        self, interaction: discord.Interaction, discord_user: str, leetcode_user: str
    ):
        await interaction.response.defer()

        if interaction.user.id in ADMINS:
            if dbfuncs.check_discord_user(discord_user):
                out = f"Discord user {discord_user} already registered"
                lc_user = dbfuncs.get_leetcode_from_discord(discord_user)
                if lc_user:
                    out += f" as {lc_user}"
                await interaction.followup.send(out)
                return

            if dbfuncs.check_leetcode_user(leetcode_user):
                out = f"User {leetcode_user} already registered"
                dc_user = dbfuncs.get_discord_from_leetcode(leetcode_user)
                if dc_user:
                    out += f" with Discord: {dc_user}"
                await interaction.followup.send(out)
                return

            dbfuncs.add_user(discord_user, leetcode_user)
            await interaction.followup.send(
                f"Registered {discord_user} as {leetcode_user}"
            )

        else:
            await interaction.followup.send("You are not an admin")


async def setup(bot):
    await bot.add_cog(AdminRegister(bot))
