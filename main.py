import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.typing = True
intents.presences = False
intents.messages = True 
intents.message_content = True


bot = commands.Bot(command_prefix='!', intents=intents)



@bot.command(name='test')
async def test_command(ctx):
    await ctx.send("Test command works!")

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        cog_name = filename[:-3]
        cog_module = f'cogs.{cog_name}'
        try:
            bot.load_extension(cog_module)
            setup_function = getattr(__import__(cog_module, fromlist=['']), 'setup', None)
            if setup_function:
                setup_function(bot)
                print(f'{cog_name} cog loaded and set up.')
            else:
                print(f'{cog_name} cog loaded but no setup function found.')
        except Exception as e:
            print(f'Error loading {cog_name} cog: {e}')

bot.run('MTE0NDYwMTA3MTMxMDg2NDQ0NQ.GW4dES.RkYBYXYmYF33ynDRoxYFIfwPIHhC2PJkTDQdcQ')
