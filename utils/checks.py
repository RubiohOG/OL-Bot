import discord

import config


def is_authorized_member(member: discord.Member) -> bool:
    if member.guild_permissions.move_members:
        return True
    if not config.ALLOWED_ROLE_IDS:
        return False
    author_roles = {role.id for role in member.roles}
    return bool(author_roles & config.ALLOWED_ROLE_IDS)
