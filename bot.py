#!/usr/bin/env python3
"""
Discord Guardian Bot – AI-powered toxicity watcher with verbose logging.
"""

from __future__ import annotations
import os
import json
import asyncio
from datetime import datetime, timedelta, timezone
from pathlib import Path
import logging

import discord
from discord.ext import commands
from dotenv import load_dotenv

from moderation import is_toxic

# ---------- logging: root configuration ----------
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(),          # DEBUG to see every payload
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("guardian")
# --------------------------------------------------



load_dotenv()


def int_env(name: str, default: int) -> int:
    raw = os.getenv(name, str(default))
    return int(raw.split()[0])

TOKEN              = os.getenv("DISCORD_BOT_TOKEN")
GUILD_ID           = os.getenv("GUILD_ID")                # optional
LOG_CHANNEL_ID     = int(os.getenv("LOG_CHANNEL_ID", "0"))
WARN_THRESHOLD     = int(os.getenv("WARN_THRESHOLD", "2"))
MUTE_DURATION_MIN  = int(os.getenv("MUTE_DURATION_MIN", "30"))

if not TOKEN:
    logger.critical("DISCORD_BOT_TOKEN missing in environment. Exiting.")
    raise SystemExit(1)

# Discord intents
intents = discord.Intents.default()
intents.message_content = True
intents.guilds          = True
intents.members         = True

bot = commands.Bot(command_prefix="!", intents=intents)

# persistent offence counter
STATE_FILE = Path(__file__).parent / "violations.json"
def load_state() -> dict[str, int]:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {}
def save_state(state: dict[str, int]) -> None:
    STATE_FILE.write_text(json.dumps(state, indent=2))

violations: dict[str, int] = load_state()


# ---------- helper: rich log embed ----------
async def log_violation(
    channel: discord.TextChannel,
    member: discord.Member,
    message: discord.Message,
    category: str,
    count: int,
):
    embed = discord.Embed(
        title=f"🚨 Toxic message detected ({category})",
        description=message.content,
        color=discord.Color.red(),
        timestamp=datetime.now(timezone.utc),
    )
    embed.set_author(name=str(member), icon_url=member.display_avatar.url)
    embed.add_field(name="Channel", value=message.channel.mention, inline=True)
    embed.add_field(name="Strike #", value=str(count), inline=True)
    await channel.send(embed=embed)
# ------------------------------------------------


@bot.event
async def on_ready() -> None:
    logger.info("Logged in as %s (id=%s)", bot.user, bot.user.id)
    logger.info("Watching guild: %s", GUILD_ID or "ALL GUILDS")
    logger.info("Warn-threshold=%s, mute after=%s min", WARN_THRESHOLD, MUTE_DURATION_MIN)


@bot.event
async def on_message(message: discord.Message) -> None:
    # ignore self + bots
    if message.author.bot:
        return

    if GUILD_ID and str(message.guild.id) != str(GUILD_ID):
        return  # message from a different server

    logger.debug("New message [%s] %s: %s",
                 message.channel, message.author, message.content)

    # ----- moderation -----
    flagged, category = is_toxic(message.content)
    logger.debug("Moderation verdict → flagged=%s, category=%s", flagged, category)

    if not flagged:
        await bot.process_commands(message)
        return

    user_id = str(message.author.id)
    strikes = violations.get(user_id, 0) + 1
    violations[user_id] = strikes
    save_state(violations)
    logger.info("User %s strike #%d (%s)", message.author, strikes, category)

    # Warn in chat
    warn_text = (
        f"⚠️ **Please keep it civil**. Detected *{category}* content. "
        f"(strike {strikes}/{WARN_THRESHOLD})"
    )
    try:
        await message.reply(warn_text, mention_author=True, delete_after=20)
    except discord.Forbidden:
        logger.warning("No permission to reply in channel %s", message.channel)

    # Log in log-channel
    log_chan = bot.get_channel(LOG_CHANNEL_ID)
    if log_chan:
        await log_violation(log_chan, message.author, message, category, strikes)

    # Mute if above threshold
    if strikes >= WARN_THRESHOLD:
        until = discord.utils.utcnow() + timedelta(minutes=MUTE_DURATION_MIN)
        try:
            await message.author.timeout(until, reason="Toxicity threshold exceeded")
            logger.info("Muted %s for %d min", message.author, MUTE_DURATION_MIN)
            if log_chan:
                await log_chan.send(
                    f"🔇 {message.author.mention} muted for {MUTE_DURATION_MIN} minutes."
                )
        except discord.Forbidden:
            logger.error("Missing permission to timeout %s", message.author)

    # hand over to other commands, if any
    await bot.process_commands(message)


if __name__ == "__main__":
    bot.run(TOKEN)
