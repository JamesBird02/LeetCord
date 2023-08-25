import discord
from discord.ext import commands
import asyncio

user_scores = {}

class LinkAccountCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        #store users leetcode information - Discord ID: leetcode_username, leetcode_url
        self.user_leetcode_information = {}
        
    @commands.command(name='add')
    async def add_account(self, ctx):
        print("Inside add_account function")
        # adds account to this server's leaderboard
        user_id = ctx.author.id
        print(f"User ID: {user_id}")

        if user_id in self.user_leetcode_information:
            await ctx.send("You already have an account linked!")
        else:
            def check_author(message):
                return message.author == ctx.author and message.content.strip() != ""
            
            try:
                print("Waiting for LeetCode username input...")
                await ctx.send("Please provide your LeetCode username:")
                leetcode_username_msg = await self.bot.wait_for('message', check=check_author, timeout=60)
                leetcode_username = leetcode_username_msg.content.strip()
                print(f"LeetCode username: {leetcode_username}")

                print("Waiting for LeetCode URL input...")
                await ctx.send("Please provide the URL to your LeetCode profile:")
                leetcode_url_msg = await self.bot.wait_for('message', check=check_author, timeout=60)
                leetcode_url = leetcode_url_msg.content.strip()
                print(f"LeetCode URL: {leetcode_url}")

                embed = discord.Embed(title="LeetCode Account Linked",
                                    description=f"Your LeetCode account '{leetcode_username}' has been linked!",
                                    color=discord.Color.green())
                await ctx.send(embed=embed)
                
                self.user_leetcode_information[user_id] = {'leetcode_username': leetcode_username, 'leetcode_url': leetcode_url}
                self.user_scores[user_id] = 0  # Initialize the user's score to 0
            except asyncio.TimeoutError:
                await ctx.send("Time ran out. Please try again later.")

def setup(bot):
    bot.add_cog(LinkAccountCog(bot))
    print("LinkAccountCog has been loaded.")