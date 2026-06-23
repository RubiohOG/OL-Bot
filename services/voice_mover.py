import asyncio
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Literal

import discord

import config
from utils.lane_rules import is_lane_one

MoveResult = Literal["moved", "skipped", "failed"]


@dataclass
class MoveStats:
    moved: int = 0
    skipped: int = 0
    failed: int = 0

    def record(self, result: MoveResult) -> None:
        if result == "moved":
            self.moved += 1
        elif result == "skipped":
            self.skipped += 1
        else:
            self.failed += 1


async def move_member(
    member: discord.Member,
    destination: discord.VoiceChannel,
) -> MoveResult:
    if member.voice is None or member.voice.channel is None:
        return "skipped"

    if member.voice.channel.id == destination.id:
        return "skipped"

    try:
        await member.move_to(destination)
    except discord.HTTPException as exc:
        if exc.status == 429:
            await asyncio.sleep(config.RATE_LIMIT_RETRY_SECONDS)
            try:
                await member.move_to(destination)
            except discord.HTTPException:
                return "failed"
        else:
            return "failed"
    else:
        await asyncio.sleep(config.MOVE_DELAY_SECONDS)
        return "moved"


async def move_members(
    members: Iterable[discord.Member],
    destination: discord.VoiceChannel,
) -> MoveStats:
    stats = MoveStats()

    for member in members:
        result = await move_member(member, destination)
        stats.record(result)

    return stats


async def split_lanes(
    members: Iterable[discord.Member],
    lane1: discord.VoiceChannel,
    lane2: discord.VoiceChannel,
) -> MoveStats:
    stats = MoveStats()

    for member in members:
        destination = lane1 if is_lane_one(member.display_name) else lane2
        result = await move_member(member, destination)
        stats.record(result)

    return stats
