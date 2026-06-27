import re

import discord
from discord.ext import commands

import config

_SINY_PATTERN = re.compile(r"\bsiny\b", re.IGNORECASE)


_NAME_SINY_PATTERN = re.compile(r"siny", re.IGNORECASE)


def _message_mentions_siny(message: discord.Message) -> bool:
    if _SINY_PATTERN.search(message.content):
        return True
    return any(
        _NAME_SINY_PATTERN.search(member.display_name)
        or _NAME_SINY_PATTERN.search(member.name)
        for member in message.mentions
    )


class Siny(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot:
            return
        if message.channel.id != config.SINY_CHANNEL_ID:
            return
        if not _message_mentions_siny(message):
            return
        await message.channel.send("Dog")
