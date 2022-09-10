import discord

from discord.ext import commands
from main import linksColl as lc

class Links(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    lcmd = discord.SlashCommandGroup(name="links", description="links commands")

    @lcmd.command(name="addlink", description="add a link to the db")
    async def addlink(self, ctx, link, name):
        await lc.update_one(
            {
                "_id": ctx.guild.id
            },
            {
                "$set": {
                    name.lower(): link
                }
            },
            upsert=True
        )

        await ctx.respond(f"link for {name} added successfully. Please note that names are set to lowercase in the database.")

    @lcmd.command(name="deletelink", description="delete a link from the db")
    async def dellink(self, ctx, name):
        doc = await lc.find_one({"_id": ctx.guild.id})
        try:
            val = doc[name]
            lc.update_one({"_id": ctx.guild.id}, {"$unset": {name: val}})
            return await ctx.respond(f"link for {name} removed.")
        except KeyError:
            return await ctx.respond("no link found by that name.")
        
    @lcmd.command(name="viewlinks", description="view Rainy's links")
    async def viewlinks(self, ctx):
        doc = await lc.find_one({"_id": ctx.guild.id})
        doc.pop("_id")
        em = discord.Embed(title="Rainy's Links!", description="View Rainy's links below!", color=discord.Color.embed_background(theme="dark"))
        em.set_thumbnail(url=ctx.guild.owner.display_avatar.url)
        for item in doc:
            ke = item
            va = doc[item]
            em.add_field(name=ke, value=f"[click here!]({va})")

        await ctx.respond(embed=em)

def setup(bot):
    bot.add_cog(Links(bot))