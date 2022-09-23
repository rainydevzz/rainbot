import discord

from main import greetColl as gc
from discord.ext import commands

class Greets(commands.Cog):
    def __init__ (self, bot):
        self.bot = bot
    
    @discord.slash_command(name="welcomesetup", description="welcome setup")
    @commands.has_permissions(administrator=True)
    async def welcome_setup(self, ctx, channel:discord.TextChannel, message):
        await gc.update_one(
            {
                "_id": ctx.guild.id
            },
            { "$set":
                {
                    "wchannel": channel.id,
                    "wmessage": message
                }
            },
            upsert=True
        )
        await ctx.respond("Setup Done!")

    @discord.slash_command(name="goodbyesetup", description="goodbye setup")
    @commands.has_permissions(administrator=True)
    async def goodbye_setup(self, ctx, channel:discord.TextChannel, message):
        await gc.update_one(
            {
                "_id": ctx.guild.id
            },
            { "$set":
                {
                    "gchannel": channel.id,
                    "gmessage": message
                }
            },
            upsert=True
        )
        await ctx.respond("Setup Done!")

    @commands.Cog.listener()
    async def on_member_join(self, member:discord.Member):
        if member.name.startswith("!"):
            member.edit(nick=member.name.replace("!", ""))

        try:
            query = {"_id": member.guild.id}  
            doc = await gc.find_one(query)
            ch = self.bot.get_channel(doc["wchannel"])
            msg = doc["wmessage"]
            em = discord.Embed(title=f"Welcome {member.name}!", description=msg, color=discord.Color.embed_background(theme="dark"))
            em.set_thumbnail(url=member.display_avatar.url)

            await ch.send(embed=em)
        except Exception as e:
            print(e)
            return

    @commands.Cog.listener()
    async def on_member_remove(self, member:discord.Member):
        try: 
            query = {"_id": member.guild.id}   
            doc = await gc.find_one(query)
            ch = self.bot.get_channel(doc["gchannel"])
            msg = doc["gmessage"]
            em = discord.Embed(title=f"Goodbye {member.name}", description=msg, color=discord.Color.embed_background(theme="dark"))
            em.set_thumbnail(url=member.display_avatar.url)

            await ch.send(embed=em)
        except Exception as e:
            print(e)
            return

def setup(bot):
    bot.add_cog(Greets(bot))