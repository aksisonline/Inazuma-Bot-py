import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta
import os

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@tasks.loop(hours=1)  # Check every hour
async def check_member_activity():
    guild = bot.get_guild(int(os.environ.get('GUILD_ID')))  # Replace YOUR_GUILD_ID with the environment variable name
    role = discord.utils.get(guild.roles, name='X')  # Replace 'X' with the role name

    for member in guild.members:
        if role not in member.roles:
            join_date = member.joined_at
            if join_date + timedelta(hours=16) <= datetime.utcnow():
                await member.kick(reason='Your time is up! See you in another realm!')

@check_member_activity.before_loop
async def before_check_member_activity():
    await bot.wait_until_ready()

    # Start the task after the bot has connected to the server
    check_member_activity.start()

bot.run(os.environ.get('TOKEN'))  # Replace YOUR_BOT_TOKEN with the environment variable name
