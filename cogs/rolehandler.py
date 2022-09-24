import discord
from discord.ext import commands
import asyncio

class RoleHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command()
    @commands.has_permissions(administrator=True)
    async def roledelete(self, ctx, filter):
        await ctx.interaction.response.send_message("deleting roles, please wait...", ephemeral=True)
        for role in ctx.guild.roles:
            if filter in role.name.lower():
                await role.delete()
                await asyncio.sleep(1.1)
            
        await ctx.interaction.edit_original_message(content="Deleted all roles under that filter!")

def setup(bot):
    bot.add_cog(RoleHandler(bot))