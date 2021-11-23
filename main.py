import discord
import os
import json
import datetime
from discord.ext import commands, tasks
from dotenv import load_dotenv


# load prefix config, assigns a prefix to each server
def get_prefix(bot, message):
    with open("prefixes.json", "r") as x:
        prefixes = json.load(x)
    return prefixes[str(message.guild.id)]


# initializing bot, prefixes, and time
bot = commands.Bot(command_prefix=get_prefix)
time = datetime.datetime.now()
current_time = time.strftime("%I:%M %p")


@bot.event  # event for when bot is ready
async def on_ready():
    change_status.start()
    print('Bot is ready. Current time:', current_time)


@tasks.loop(seconds=30)  # loop that updates the bot's time status every 30 seconds
async def change_status():
    time = datetime.datetime.now()
    current_time = time.strftime("%I:%M %p")
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name="NY Time: " + current_time))


@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')


@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')


@bot.command()
async def reload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    bot.load_extension(f'cogs.{extension}')


filecount = 0
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        filecount = filecount + 1
        bot.load_extension(f'cogs.{filename[:-3]}')

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot.run(TOKEN)

# Cog Tester - Not working yet
if filecount == len(os.listdir('./cogs')):
    print('All cogs online.')
elif filecount < len(os.listdir('./cogs')):
    print('Some cogs offline.')
elif filecount > len(os.listdir('./cogs')):
    print('Too many cogs online.')

# invite link
# https://discord.com/api/oauth2/authorize?client_id=901602355437522965&permissions=8&scope=bot
# dev dump server id
# 813941027169239100
