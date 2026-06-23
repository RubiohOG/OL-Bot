import discord
from discord.ext import commands

import config
from services.lane_channels import author_in_lane_vc, collect_lane_members, get_lane_channels
from services.voice_mover import split_lanes
from utils.checks import is_authorized_member
from utils.embeds import send_move_summary


class Lane(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(name="lane", aliases=["lanes"])
    @commands.guild_only()
    @commands.cooldown(1, config.COMMAND_COOLDOWN_SECONDS, commands.BucketType.user)
    async def lane(self, ctx: commands.Context) -> None:
        """Split users between Lane 1 and Lane 2 based on a display name prefix of '1'."""
        if not isinstance(ctx.author, discord.Member):
            return

        channels = get_lane_channels(ctx.guild)
        if channels is None:
            await ctx.send("Error: configured voice channels were not found.")
            return

        lane1, lane2 = channels

        in_lane = author_in_lane_vc(ctx.author, lane1, lane2)
        if not in_lane and not is_authorized_member(ctx.author):
            await ctx.send("You must be in Lane 1 or Lane 2 to use this command.")
            return

        members = collect_lane_members(lane1, lane2)
        if not members:
            await ctx.send("No users are in the lanes.")
            return

        stats = await split_lanes(members, lane1, lane2)
        await send_move_summary(ctx, "Lanes split", stats)

    @lane.error
    async def lane_error(self, ctx: commands.Context, error: commands.CommandError) -> None:
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"Please wait {error.retry_after:.0f}s before using this command again.")
            return
        raise error
