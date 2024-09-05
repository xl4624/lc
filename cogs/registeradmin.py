import discord
from discord.ext import commands
from discord import app_commands
from lib.admins import ADMINS
import lib.dbfuncs as dbfuncs


class AdminRegisterAdmin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Admin Register new Admin cog loaded")

    @app_commands.command(
        name="zregisteradmin", description="Register a new admin (ADMIN ONLY)"
    )
    @app_commands.describe(discord_id="discord ID to register")
    async def adminregisteradmin(
        self, interaction: discord.Interaction, discord_id: int
    ):
        await interaction.response.defer()

        if interaction.user.id in ADMINS:
            # insert discord_id to admin table
            if dbfuncs.add_admin(discord_id):
                await interaction.followup.send(f"Registered {discord_id} as new admin")
            else:
                await interaction.followup.send(
                    f"Failed to register {discord_id} as new admin"
                )

        else:
            await interaction.followup.send("You are not an admin")


async def setup(bot):
    await bot.add_cog(AdminRegisterAdmin(bot))
