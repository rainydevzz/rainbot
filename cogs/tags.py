import discord
from discord.ext import commands
from main import tagsColl as tc

class Tags(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    tagcmd = discord.SlashCommandGroup(name="tags", description="tags commands")

    @tagcmd.command(name="add", description="add or update a tag")
    async def add(self, ctx, name, content):
        await tc.update_one({"_id": ctx.guild.id}, {"$set": {name.lower(): content}}, upsert=True)
        await ctx.respond(f"tag `{name}` added!")

    @tagcmd.command(name="remove", description="remove a tag")
    async def remove(self, ctx, name):
        try:   
            doc = await tc.find_one({"_id": ctx.guild.id})
            await tc.update_one({"_id": ctx.guild.id}, {"$unset": {name.lower(): doc[name]}})
            await ctx.respond(f"tag `{name}` removed!")

        except:
            await ctx.respond("could not find that tag.")

    @tagcmd.command(name="viewall", description="view all tags")
    async def viewall(self, ctx):
        doc = await tc.find_one({"_id": ctx.guild.id})
        doc.pop("_id")
        dstr = ""

        for item in doc.keys():
            dstr += f"`{item}`\n"

        em = discord.Embed(title="Tags", description=dstr, color=discord.Color.embed_background(theme="dark"))
        await ctx.respond(embed=em)

    @tagcmd.command(name="view", description="view a tag")
    async def view(self, ctx, name):
        doc = await tc.find_one({"_id": ctx.guild.id})
        doc.pop("_id")
        try:
            tag = doc[name.lower()]
            await ctx.respond(tag)

        except:
            await ctx.respond("could not find that tag.")

def setup(bot):
    bot.add_cog(Tags(bot))