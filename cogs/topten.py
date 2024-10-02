import discord
from discord.ext import commands
from discord import app_commands
import requests
import datetime

class TopTen(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.is_mobile_view = False

    @commands.Cog.listener()
    async def on_ready(self):
        print("Top 10 cog loaded")

    @app_commands.command(
        name="top10",
        description="View the top 10 users.",
    )
    async def top10(self, interaction: discord.Interaction):
        await interaction.response.defer()
        try:
            url = 'https://server.rakibshahid.com/leaderboard'
            response = requests.get(url)
            data = response.json()
            embed = self.create_detailed_embed(data, interaction.user.name)

            view = discord.ui.View()
            toggle_button = discord.ui.Button(label="Toggle View", style=discord.ButtonStyle.primary)
            view.add_item(toggle_button)

            message = await interaction.followup.send(embed=embed, view=view)

            async def button_callback(interaction: discord.Interaction):
                self.is_mobile_view = not self.is_mobile_view
                new_embed = self.create_mobile_embed(data, interaction.user.name) if self.is_mobile_view else self.create_detailed_embed(data, interaction.user.name)
                await interaction.response.edit_message(embed=new_embed)

            toggle_button.callback = button_callback
            
        except Exception as e:
            print(e)

    def create_mobile_embed(self, data, user_name):
        description = ''
        leetcode_emoji = self.bot.get_emoji(1290903612351844464)
        discord_emoji = self.bot.get_emoji(1290903900169310248)
        for i in range(10):
            description += f"{i + 1}. {discord_emoji}{data[i]['discord_username']} ({leetcode_emoji}{data[i]['username']}) - {data[i]['points']} \n"
        embed = discord.Embed(title="Top 10 Users - Mobile View", description=description, timestamp=datetime.datetime.now())
        embed.set_footer(text=f"Requested by {user_name}")
        return embed

    def create_detailed_embed(self, data, user_name):
        embed = discord.Embed(title="Top 10 Users", timestamp=datetime.datetime.utcnow())
        leetcode_emoji = self.bot.get_emoji(1290903612351844464)
        discord_emoji = self.bot.get_emoji(1290903900169310248)
        discord_users = []
        leetcode_users = []
        points = []
        for i in range(10):
            leetcode_users.append(data[i]['username'])
            discord_users.append(f"{data[i]['discord_username']}")
            points.append(data[i]['points'])
        embed.add_field(name=f"{discord_emoji} Discord User", value="\n".join(discord_users), inline=True)
        embed.add_field(name=f"{leetcode_emoji} Leetcode User", value="\n".join(leetcode_users), inline=True)
        embed.add_field(name="Points", value="\n".join(map(str, points)), inline = True)
        embed.set_footer(text=f"Requested by {user_name}")
        return embed

async def setup(bot):
    await bot.add_cog(TopTen(bot))
