import discord
from discord.ext import commands

class ErrorHandler(discord.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.Cog.listener()
    async def on_application_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            return await ctx.respond("You do not have permission to run this command.", ephemeral=True)

        else:
            return await ctx.respond(f"**An error has occurred!**\n\n```{error}```")

def setup(bot):
    bot.add_cog(ErrorHandler(bot))