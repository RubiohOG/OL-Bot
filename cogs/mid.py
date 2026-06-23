import discord
from discord.ext import commands

import config
from services.lane_channels import author_in_lane_vc, collect_lane_members, get_lane_channels
from services.voice_mover import move_members
from utils.checks import is_authorized_member
from utils.embeds import send_move_summary


class Mid(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(name="mid")
    @commands.guild_only()
    @commands.cooldown(1, config.COMMAND_COOLDOWN_SECONDS, commands.BucketType.user)
    async def mid(self, ctx: commands.Context) -> None:
        """Move all users from both lanes into your voice channel."""
        if not isinstance(ctx.author, discord.Member):
            return

        if ctx.author.voice is None or ctx.author.voice.channel is None:
            await ctx.send("You must be in a voice channel to use this command.")
            return

        destination = ctx.author.voice.channel
        if not isinstance(destination, discord.VoiceChannel):
            await ctx.send("You must be in a voice channel to use this command.")
            return

        channels = get_lane_channels(ctx.guild)
        if channels is None:
            await ctx.send("Error: configured voice channels were not found.")
            return

        lane1, lane2 = channels

        in_lane = author_in_lane_vc(ctx.author, lane1, lane2)
        if not in_lane and not is_authorized_member(ctx.author):
            await ctx.send(
                "You must be in Lane 1, Lane 2, or have moderator permission to use this command."
            )
            return

        members = collect_lane_members(lane1, lane2)
        if not members:
            await ctx.send("No users are in the lanes.")
            return

        stats = await move_members(members, destination)
        await send_move_summary(ctx, "Users gathered in mid", stats)

    @mid.error
    async def mid_error(self, ctx: commands.Context, error: commands.CommandError) -> None:
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"Please wait {error.retry_after:.0f}s before using this command again.")
            return
        raise error
