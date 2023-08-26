import discord
import asyncio
from datetime import datetime
import random
from discord.ext import commands
from discord import interactions
import database
from discord.ext import commands, tasks
from discord import app_commands
import json
import requests
import sqlite3
import database
import interactions
from discord import app_commands
import os
from dotenv import load_dotenv
import os

load_dotenv()

token =  os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()

intents.typing = True
intents.presences = False
intents.messages = True 
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)




@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
        
# @bot.command()
# async def help(ctx):
#     #help message
#     embed = discord.Embed(title="LeetCode Bot Help", description="Here are the commands you can use with the LeetCode Bot:", color=discord.Color.green())


def fetch_user_stats(username):
    try:
        # API request to fetch LeetCode user statistics
        response = requests.get(f"https://leetcode-stats-api.herokuapp.com/{username}")
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print("Error fetching LeetCode statistics:", e)
        return None

@bot.command()
async def question(ctx):

    try:
        response = requests.get("https://leetcode.com/api/problems/algorithms/")
        data = response.json()

        if 'stat_status_pairs' in data:
            problems = data['stat_status_pairs']
            random_problem = random.choice(problems)

            question_title = random_problem['stat']['question__title']
            question_slug = random_problem['stat']['question__title_slug']
            difficulty = random_problem['difficulty']['level']
            acceptance = random_problem['stat']['total_acs'] / random_problem['stat']['total_submitted'] * 100
            
            difficulty_mapping = {
                1: ("Easy", discord.Color.green()),
                2: ("Medium", discord.Color.gold()),
                3: ("Hard", discord.Color.red())
            }

            difficulty_text, embed_color = difficulty_mapping.get(difficulty, ("Unknown", discord.Color.default()))

            # Create an embedded message
            embed = discord.Embed(title=f"{question_title}", color=embed_color)
            embed.add_field(name="Difficulty", value=f"{difficulty_text.capitalize()}", inline=True)
            embed.add_field(name="Acceptance Rate", value=f"{acceptance:.2f}%", inline=True)
            embed.add_field(name="Question Link", value=f"[Click here](https://leetcode.com/problems/{question_slug}/)")

            await ctx.send(embed=embed)

        else:
            await ctx.send("Error: Unable to fetch problem, please try again later.")

    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")





@bot.command(name="register", description="Register your LeetCode profile")
async def register(ctx):
    user_id = str(ctx.author.id)
    existing_profile = database.get_user_profile(user_id)
    
    if existing_profile:
        await ctx.author.send("You already have a profile registered. Would you like to overwrite it? (y/n)")
        
        try:
            overwrite_response = await bot.wait_for("message", check=lambda message: message.author == ctx.author and isinstance(message.channel, discord.DMChannel), timeout=20)
            overwrite_response_content = overwrite_response.content.lower()

            if overwrite_response_content == "y":
                await ctx.author.send("Please enter your LeetCode username.")

                user_response = await bot.wait_for("message", check=lambda message: message.author == ctx.author and isinstance(message.channel, discord.DMChannel), timeout=80)
                leetcode_username = user_response.content

                # Check if the username is valid using the LeetCode API
                user_stats = fetch_user_stats(leetcode_username)

                if user_stats.get("status") == "success":
                    database.update_user_profile(user_id, leetcode_username)
                    await ctx.author.send(f"Profile updated with LeetCode username: {leetcode_username}")
                else:
                    await ctx.author.send("Invalid LeetCode username. Profile update canceled.")

            else:
                await ctx.author.send("Profile registration canceled.")

        except asyncio.TimeoutError:
            await ctx.author.send("Registration timed out.")
    else:
        await ctx.author.send("Please enter your LeetCode username.")

        try:
            user_response = await bot.wait_for("message", check=lambda message: message.author == ctx.author and isinstance(message.channel, discord.DMChannel), timeout=80)
            leetcode_username = user_response.content

            # Check if the username is valid using the LeetCode API
            user_stats = fetch_user_stats(leetcode_username)

            if user_stats.get("status") == "success":
                database.register_user(user_id, leetcode_username)
                await ctx.author.send(f"Successfully registered {leetcode_username}!")
            else:
                await ctx.author.send("Invalid LeetCode username. Registration canceled.")

        except asyncio.TimeoutError:
            await ctx.author.send("Registration timed out.")





@bot.command(name="stats", description="Fetch LeetCode statistics")
async def stats(ctx, user: discord.User = None):
    if user is None:
        user = ctx.author

    leetcode_username = database.get_leetcode_id(str(user.id))

    if not leetcode_username:
        await ctx.send(f"{user.mention} is not registered in the database.")
        return

    try:
        # API request to fetch LeetCode user statistics
        response = requests.get(f"https://leetcode-stats-api.herokuapp.com/{leetcode_username}")
        user_stats = response.json()

        if user_stats.get("status") == "success":
            embed = discord.Embed(title=f"LeetCode Stats for {leetcode_username}", color=discord.Color.blue())
            embed.add_field(name="Total Solved", value=user_stats["totalSolved"], inline=True)
            embed.add_field(name="Easy Solved", value=user_stats["easySolved"], inline=True)
            embed.add_field(name="Medium Solved", value=user_stats["mediumSolved"], inline=True)
            embed.add_field(name="Hard Solved", value=user_stats["hardSolved"], inline=True)
            embed.add_field(name="Acceptance Rate", value=f"{user_stats['acceptanceRate']:.2f}%", inline=True)
            embed.add_field(name="Ranking", value=user_stats["ranking"], inline=True)
            
            await ctx.send(content=f"{user.mention}", embed=embed)
        else:
            await ctx.send("Unable to fetch LeetCode statistics for the provided username.")
    except Exception as e:
        print(f"Error fetching LeetCode statistics: {e}")
        await ctx.send("An error occurred while fetching LeetCode statistics.")





bot.run(token)
