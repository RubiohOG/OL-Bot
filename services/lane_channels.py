import discord

import config


def get_lane_channels(
    guild: discord.Guild,
) -> tuple[discord.VoiceChannel, discord.VoiceChannel] | None:
    lane1 = guild.get_channel(config.LANE_1_CHANNEL_ID)
    lane2 = guild.get_channel(config.LANE_2_CHANNEL_ID)

    if not isinstance(lane1, discord.VoiceChannel):
        return None
    if not isinstance(lane2, discord.VoiceChannel):
        return None
    return lane1, lane2


def collect_lane_members(
    lane1: discord.VoiceChannel,
    lane2: discord.VoiceChannel,
) -> list[discord.Member]:
    seen: set[int] = set()
    members: list[discord.Member] = []

    for channel in (lane1, lane2):
        for member in channel.members:
            if member.bot or member.id in seen:
                continue
            seen.add(member.id)
            members.append(member)

    return members


def author_in_lane_vc(
    author: discord.Member,
    lane1: discord.VoiceChannel,
    lane2: discord.VoiceChannel,
) -> bool:
    if author.voice is None or author.voice.channel is None:
        return False
    channel_id = author.voice.channel.id
    return channel_id in (lane1.id, lane2.id)
