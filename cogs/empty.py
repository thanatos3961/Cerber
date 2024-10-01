import discord
from discord.ext import commands

Denied_emoji = "<:WrenchDenied:1281769128633569330>"
Checkmark_emoji = "<:WrenchCheckmark:1281769061763649536>"

embed_color = discord.Color.red()
unsuccessful_color = discord.Color.orange()

class EMPTY(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.command(name="hi")
    async def hello(self, ctx: commands.Context):
        await ctx.reply("hi")

async def setup(bot: commands.Bot):
    await bot.add_cog(EMPTY(bot))
