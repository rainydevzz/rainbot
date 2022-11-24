import discord
import asyncio

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

def setup(bot):
    bot.add_cog(UtilsCog(bot))