import discord
from discord.ext import commands
from main import tagsColl as tc

class Tags(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    tagcmd = discord.SlashCommandGroup(name="tags", description="tags commands")

    @tagcmd.command(name="add", description="add or update a tag")
    @commands.has_permissions(administrator=True)
    async def add(self, ctx: discord.ApplicationContext, name: str, content: str):
        await tc.update_one({"_id": str(ctx.guild.id)}, {"$set": {name.lower(): content}}, upsert=True)
        await ctx.respond(f"tag `{name}` added!")

    @tagcmd.command(name="remove", description="remove a tag")
    @commands.has_permissions(administrator=True)
    async def remove(self, ctx: discord.ApplicationContext, name: str):
        try:   
            doc = await tc.find_one({"_id": str(ctx.guild.id)})
            await tc.update_one({"_id": str(ctx.guild.id)}, {"$unset": {name.lower(): doc[name]}})
            await ctx.respond(f"tag `{name}` removed!")

        except:
            await ctx.respond("could not find that tag.")

    @tagcmd.command(name="viewall", description="view all tags")
    async def viewall(self, ctx: discord.ApplicationContext):
        doc = await tc.find_one({"_id": str(ctx.guild.id)})
        doc.pop("_id")

        em = discord.Embed(title="Tags", description=", ".join(list(doc.keys())), color=discord.Color.embed_background(theme="dark"))
        await ctx.respond(embed=em)

    @tagcmd.command(name="view", description="view a tag")
    async def view(self, ctx: discord.ApplicationContext, name: str):
        doc = await tc.find_one({"_id": str(ctx.guild.id)})
        doc.pop("_id")
        try:
            tag = doc[name.lower()]
            await ctx.respond(tag)

        except:
            await ctx.respond("could not find that tag.")

def setup(bot):
    bot.add_cog(Tags(bot))
