# OL Bot

Discord bot for League-style lane voice management. Splits players between two lane voice channels or gathers everyone into the caller's channel.

## Setup

1. Copy `.env.example` to `.env` and fill in your values.
2. Install dependencies: `pip install -r requirements.txt`
3. Run: `python bot.py`

## Commands

| Command | Description |
|---------|-------------|
| `!lane` / `!lanes` | Split users in Lane 1 and Lane 2 by display name (prefix `1` → Lane 1) |
| `!mid` | Move all lane users into your current voice channel |

The default help command is disabled to avoid listing commands publicly.

## Required Discord Configuration

- **Bot permissions:** Move Members, View Channels, Connect, Send Messages
- **Privileged intents:** Message Content Intent (Developer Portal → Bot)
- **Role hierarchy:** The bot role must be above roles of users you want to move

## Security & Trust Model

### Who can run commands

Both commands require the caller to meet **one** of these conditions:

1. **Lane voice channel** — be connected to Lane 1 or Lane 2 (configured via `LANE_1_CHANNEL_ID` / `LANE_2_CHANNEL_ID`)
2. **Moderator access** — have the Discord **Move Members** permission, or a role listed in `ALLOWED_ROLE_IDS`

This prevents members in unrelated voice channels (e.g. AFK, General) from moving lane players.

### Rate limiting

Each user has a cooldown between command uses (default 30 seconds, configurable via `COMMAND_COOLDOWN_SECONDS`).

### Lane assignment logic

`!lane` assigns users by display name: names starting with `1` (after whitespace) go to Lane 1. Users can change their display name to influence assignment — this is intentional game logic, not a code vulnerability.

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `DISCORD_TOKEN` | Yes | Bot token from Discord Developer Portal |
| `LANE_1_CHANNEL_ID` | Yes | Voice channel ID for Lane 1 |
| `LANE_2_CHANNEL_ID` | Yes | Voice channel ID for Lane 2 |
| `COMMAND_PREFIX` | No | Prefix for commands (default `!`) |
| `ALLOWED_ROLE_IDS` | No | Comma-separated role IDs that may run commands without being in a lane VC |
| `COMMAND_COOLDOWN_SECONDS` | No | Per-user cooldown in seconds (default `30`) |

## Secret Handling

- **Never commit `.env`** — it is listed in `.gitignore` along with `.env.local` and `*.pem`.
- Use `.env.example` as the template only; it contains placeholders, not real secrets.
- If a token is ever exposed (committed, shared, or pasted), **rotate it immediately** in the [Discord Developer Portal](https://discord.com/developers/applications) → your app → Bot → Reset Token.
- Run `git status` before your first commit and confirm `.env` does not appear in untracked or staged files.

## Dependency Security

Dependencies are pinned in `requirements.txt`. Periodically audit with:

```bash
pip install pip-audit
python -m pip_audit -r requirements.txt
```

## Project Structure

```
bot.py              Entry point
config.py           Environment loading
cogs/               Command handlers (lane, mid)
services/           Voice move logic and channel resolution
utils/              Auth checks, embeds, lane rules
```
