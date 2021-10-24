import discord
import json
from discord import member
from discord.ext import commands

class Events(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(guild):
        with open("prefixes.json", "r") as x:
            prefixes = json.load(x)
        prefixes[str(guild.id)] = "!"
        with open("prefixes.json", "w") as x:
            json.dump(prefixes, x, indent = 4)

    @commands.Cog.listener()
    async def on_guild_remove(guild):
        with open("prefixes.json", "r") as x:
            prefixes = json.load(x)
        prefixes.pop(str(guild.id))
        with open("prefixes.json", "w") as x:
            json.dump(prefixes, x, indent = 4)
    
    @commands.Cog.listener()
    async def on_member_join(member):
        await member.create_dm()
        await member.dm_channel.send(f"Welcome to the Ashvin's Development Server, {member.name}!")
    
    @commands.Cog.listener()
    async def on_member_remove(member):
        await member.create_dm()
        await member.dm_channel.send(f"Goodbye, {member.name}!")
            
def setup(bot):
    bot.add_cog(Events(bot))
