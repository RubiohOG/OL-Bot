import os
import sys

from dotenv import load_dotenv

load_dotenv()


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        print(f"Error: missing environment variable {name}. Copy .env.example to .env and fill it in.")
        sys.exit(1)
    return value


def _require_int_env(name: str) -> int:
    raw = _require_env(name)
    try:
        return int(raw)
    except ValueError:
        print(f"Error: {name} must be a numeric ID, got: {raw!r}")
        sys.exit(1)


def _parse_role_ids(raw: str | None) -> frozenset[int]:
    if not raw or not raw.strip():
        return frozenset()
    ids: set[int] = set()
    for part in raw.split(","):
        part = part.strip()
        if not part:
            continue
        try:
            ids.add(int(part))
        except ValueError:
            print(f"Error: invalid role ID in ALLOWED_ROLE_IDS: {part!r}")
            sys.exit(1)
    return frozenset(ids)


DISCORD_TOKEN = _require_env("DISCORD_TOKEN")
LANE_1_CHANNEL_ID = _require_int_env("LANE_1_CHANNEL_ID")
LANE_2_CHANNEL_ID = _require_int_env("LANE_2_CHANNEL_ID")
COMMAND_PREFIX = os.getenv("COMMAND_PREFIX", "!")
ALLOWED_ROLE_IDS = _parse_role_ids(os.getenv("ALLOWED_ROLE_IDS"))

MOVE_DELAY_SECONDS = 0.8
RATE_LIMIT_RETRY_SECONDS = 2.0
COMMAND_COOLDOWN_SECONDS = float(os.getenv("COMMAND_COOLDOWN_SECONDS", "10"))

SINY_CHANNEL_ID = int(os.getenv("SINY_CHANNEL_ID", "651138824751022111"))
