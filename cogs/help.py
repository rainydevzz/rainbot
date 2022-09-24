import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command()
    async def help(self, ctx):
        em = discord.Embed(title="Help", description="RainBot's Help Commands! <3", color=discord.Color.embed_background(theme="dark"))
        em.set_thumbnail(url=self.bot.user.avatar.url)
        cmdstr = ""
        for cogname, cog in self.bot.cogs.items():
            cogcmds = cog.walk_commands()
            for command in cogcmds:
                cmdstr += f"{command.name}\n"
            em.add_field(name=cogname, value=cmdstr)
            cmdstr = ""
            
        await ctx.respond(embed=em, ephemeral=True)

def setup(bot):
    bot.add_cog(Help(bot))