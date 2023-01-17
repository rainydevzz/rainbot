import discord
import asyncio
import datetime

from discord.ui import Modal, InputText
from discord.ext import commands

class EmbedModal(Modal):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.add_item(InputText(label="Title"))
        self.add_item(InputText(label="Description", style=discord.InputTextStyle.long))
        self.add_item(InputText(label="Channel ID"))

    async def callback(self, inter: discord.Interaction):
        em = discord.Embed(title=self.children[0].value, description=self.children[1].value)
        ch = inter.client.get_channel(int(self.children[2].value))
        em.set_footer(text="Embed Builder!", icon_url=inter.client.user.avatar.url)
        await ch.send(embed=em)
        await inter.response.send_message("Embed Sent!", ephemeral=True)

class UtilsCog(discord.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command()
    @commands.has_permissions(manage_guild=True)
    async def buildembed(self, ctx):
        modal = EmbedModal(title="Embed Builder")
        await ctx.send_modal(modal)

    @discord.slash_command()
    @commands.has_permissions(administrator=True)
    async def roledelete(self, ctx, filter):
        await ctx.interaction.response.send_message("deleting roles, please wait...", ephemeral=True)
        for role in ctx.guild.roles:
            if filter in role.name.lower():
                await role.delete()
                await asyncio.sleep(1.1)
            
        await ctx.interaction.edit_original_message(content="Deleted all roles under that filter!")

    @discord.slash_command()
    async def about(self, ctx):
        em = discord.Embed(title=f"About {self.bot.user.name}", description="Private bot for Rainy's server.", color=0x90ee90)
        em.add_field(name="Dev", value="Rainy~#2571")
        em.add_field(name="Library", value=f"Pycord {discord.__version__}")
        em.set_thumbnail(url=self.bot.user.avatar.url)
        await ctx.respond(embed=em)

    @discord.slash_command()
    async def memberinfo(self, ctx, member: discord.Option(discord.Member, "user to select", required=False)):
        if member is None:
            member = ctx.author
        roles = ', '.join([r.name for r in member.roles if not r.name == "@everyone"])
        if roles == '':
            roles = "No Roles"
        print(roles)
        em = discord.Embed(title=f"Info for {member.name}", description="Date Format is M-D-Y", color=discord.Color.green())
        em.add_field(name="Joined At", value=member.joined_at.strftime("%m/%d/%Y"))
        em.add_field(name="Created At", value=member.created_at.strftime('%m/%d/%Y'))
        em.add_field(name="Roles", value=f"```\n{roles}\n```")
        em.set_thumbnail(url=member.avatar.url)
        em.timestamp = datetime.datetime.now()
        await ctx.respond(embed=em)

    @discord.slash_command()
    @commands.has_permissions(manage_roles=True)
    async def addrole(self, ctx, member:discord.Member, role:discord.Role):
        em = discord.Embed(description=f"Gave Role {role.mention} to {member.mention}", color=0x90ee90)
        await member.add_roles(role, reason="RainBot Role Add")
        await ctx.respond(embed=em, ephemeral=True)

    @discord.slash_command()
    @commands.has_permissions(manage_roles=True)
    async def removerole(self, ctx, member:discord.Member, role:discord.Role):
        em = discord.Embed(description=f"Removed Role {role.mention} from {member.mention}", color=0xff0000)
        await member.remove_roles(role, reason="RainBot Role Remove")
        await ctx.respond(embed=em, ephemeral=True)

def setup(bot):
    bot.add_cog(UtilsCog(bot))