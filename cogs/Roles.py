import discord
import json
from discord import member
from discord.ext import commands

class Roles(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
            
def setup(bot):
    bot.add_cog(Roles(bot))
