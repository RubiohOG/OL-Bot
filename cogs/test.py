import discord
from discord.ext import commands


class Test(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(name="test")
    @commands.guild_only()
    async def test(self, ctx: commands.Context) -> None:
        """Check that the bot is online and responding."""
        latency_ms = round(self.bot.latency * 1000)
        await ctx.send(f"Bot online. Latency: {latency_ms} ms")
