import discord
from discord.ext import commands
from discord import app_commands
import lib.dbfuncs as dbfuncs
import requests
import datetime


class Lookup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Lookup cog loaded")

    @app_commands.command(
        name="lookup",
        description="Lookup a user on the leaderboard by discord or leetcode username.",
    )
    @app_commands.describe(username="enter discord or leetcode username")
    async def lookup(self, interaction: discord.Interaction, username: str):
        await interaction.response.defer()
        embed = discord.Embed(title=f"User Lookup - {username}", timestamp=datetime.datetime.now())
        sad = self.bot.get_emoji(1110418413920206868)
        embed.set_footer(text=f"Requested by {interaction.user.name}")
        description = f'User {username} not found {sad if sad else ":cry:"}'
        embed.set_image(url="https://media1.tenor.com/m/lxJgp-a8MrgAAAAd/laeppa-vika-half-life-alyx.gif")
        urls = ["https://server.rakibshahid.com/api/discord_lookup", "https://server.rakibshahid.com/api/leetcode_lookup"]
        header_titles = ["discord-username", "leetcode-username"]
        leetcode_emoji = self.bot.get_emoji(1290903612351844464)
        discord_emoji = self.bot.get_emoji(1290903900169310248)
        for url, header_title in zip(urls, header_titles):
            response = requests.get(url, headers={header_title: username})
            try:
                if response.status_code == 200:
                    data = response.json()
                    description = f"{discord_emoji} **Discord Username**: {data['discord_username']}\n"
                    description += f"{leetcode_emoji} **LeetCode Username**: {data['leetcode_username']}\n"
                    points = dbfuncs.get_user_points(data['discord_username'])
                    description += f":chart_with_upwards_trend: **Points**: {points}\n"
                    description += f":crown: **Wins**: {data['wins']}\n"
                    
                    description += f":1234: **Local Rank**: {data['local_ranking']}\n"
                    # format global rank with commas
                    global_ranking = "{:,}".format(data['ranking'])
                    description += f":earth_americas: **Global LeetCode Rank**: {global_ranking}\n"
                    
                    embed.set_image(url=data['avatar'])
                        
                    break
            except Exception as e:
                print(e)
        embed.description = description

        
        
        await interaction.followup.send(
            embed = embed
        )


async def setup(bot):
    await bot.add_cog(Lookup(bot))
