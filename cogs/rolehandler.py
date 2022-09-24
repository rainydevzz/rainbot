import discord
from discord.ext import commands
import asyncio

class RoleHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command()
    @commands.has_permissions(administrator=True)
    async def roledelete(self, ctx, filter):
        await ctx.defer()
        for role in ctx.guild.roles:
            if filter in role.name.lower():
                await role.delete()
                await asyncio.sleep(2.5)
            
        await ctx.respond("Deleted all roles under that filter!", ephemeral=True)

def setup(bot):
    bot.add_cog(RoleHandler(bot))