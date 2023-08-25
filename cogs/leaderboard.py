import discord
from discord.ext import commands
import datetime
from .link_account import user_scores

class LeaderboardCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.week_start = datetime.datetime.utcnow()

    def reset_week_score(self):
        self.user_scores = {user_id: 0 for user_id in self.user_scores}
        self.week_start = datetime.datetime.utcnow()

    def gen_leaderboard(self):
        now = datetime.datetime.utcnow()
        last_week = now - datetime.timedelta(days=7)

        sorted_users = sorted(user_scores.items(), key=lambda item: item[1], reverse=True)
        top_users = sorted_users[:10]

        leaderboard_text = "Weekly Top 10 Leaderboard:\n"

        for position, (user_id, score) in enumerate(top_users, start=1):
            user = self.bot.get_user(user_id)
            if user:
                leaderboard_text += f"{position}. {user.display_name} - Score {score}\n"

        return leaderboard_text
    
    @commands.command(name='leaderboard')
    async def leaderboard(self, ctx):
        leaderboard_text = self.gen_leaderboard()
        await ctx.send(leaderboard_text)

def setup(bot):
    bot.add_cog(LeaderboardCog(bot))
