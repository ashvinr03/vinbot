import discord
import json
from discord import member
from discord.ext import commands


class BaseCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send('Pong!')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f'Kicked {member.mention}')

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('You do not have permission to kick members.')
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('You need to specify a member to kick.')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f'Banned {member.mention}')

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('You do not have permission to ban members.')
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('You need to specify a member to ban.')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'Unbanned {user.name}#{user.discriminator}')
                return

    @commands.command()
    @commands.has_permissions(mute_members=True)
    async def mute(self, ctx, member: discord.Member, *, reason=None):
        await member.add_roles(discord.utils.get(ctx.guild.roles, name="Muted"))
        await ctx.send(f'Muted {member.mention}')

    @commands.command()
    @commands.has_permissions(mute_members=True)
    async def unmute(self, ctx, member: discord.Member, *, reason=None):
        await member.remove_roles(discord.utils.get(ctx.guild.roles, name="Muted"))
        await ctx.send(f'Unmuted {member.mention}')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def changeprefix(self, ctx, prefix):
        with open('prefixes.json', 'r') as x:
            prefixes = json.load(x)
        prefixes[str(ctx.guild.id)] = prefix
        with open('prefixes.json', 'w') as x:
            json.dump(prefixes, x, indent=4)
        await ctx.send(f'Prefix changed to {prefix}')


def setup(bot):
    bot.add_cog(BaseCommands(bot))
