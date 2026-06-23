import discord
from discord.ext import commands

from services.voice_mover import MoveStats


def build_move_summary_embed(
    title: str,
    moved: int,
    skipped: int,
    failed: int,
) -> discord.Embed:
    embed = discord.Embed(title=title, color=discord.Color.green())
    embed.add_field(name="Moved", value=str(moved), inline=True)
    embed.add_field(name="Skipped", value=str(skipped), inline=True)
    embed.add_field(name="Failed", value=str(failed), inline=True)
    return embed


async def send_move_summary(
    ctx: commands.Context,
    title: str,
    stats: MoveStats,
) -> None:
    embed = build_move_summary_embed(title, stats.moved, stats.skipped, stats.failed)
    await ctx.send(embed=embed)
