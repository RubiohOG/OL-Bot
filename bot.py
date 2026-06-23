import discord
from discord.ext import commands

import config
from cogs.lanes import Lane
from cogs.mid import Mid


class OLBot(commands.Bot):
    async def setup_hook(self) -> None:
        await self.add_cog(Lane(self))
        await self.add_cog(Mid(self))


def main() -> None:
    intents = discord.Intents.default()
    intents.members = True
    intents.voice_states = True
    intents.message_content = True

    bot = OLBot(command_prefix=config.COMMAND_PREFIX, intents=intents, help_command=None)

    @bot.event
    async def on_ready() -> None:
        print(f"Logged in as {bot.user} (ID: {bot.user.id})")

    bot.run(config.DISCORD_TOKEN)


if __name__ == "__main__":
    main()
