# Discord Guardian Bot 🛡️

AI‑powered moderation assistant that **detects toxic messages in real‑time** and
keeps your community safe.

![demo gif placeholder](https://user-images.githubusercontent.com/your-demo.gif)

---

## ✨ What it does

1. Listens to every message in your server.
2. Sends content to **OpenAI’s moderation endpoint**.
3. If flagged (*hate, harassment, violence, etc.*):
   * Replies with a polite warning.
   * Records the offence count.
   * After *N* violations, automatically **mutes** (timeout) the user for a configurable duration.
4. Logs actions in a dedicated `#moderation-log` channel.

All behaviour (thresholds, mute duration, guild restriction) is controlled via
environment variables.

---

## 🏗️ Tech stack

| Layer | Choice | Rationale |
|-------|--------|-----------|
| Discord client | `discord.py` 2.x | Robust, slash‑command ready |
| AI moderation | `omni-moderation-latest` | Best coverage for hateful/violent content |
| Config | `.env` + `python-dotenv` | Simple secrets management |
| Persistence | `violations.json` | Lightweight for hack‑project scope |
| Container | Dockerfile | Easy deploy on Fly.io, Railway, etc. |

---

## 🚀 Quickstart

```bash
git clone <your-fork> discord_guardian_bot
cd discord_guardian_bot
cp .env.example .env   # fill tokens and IDs

python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python bot.py
```

> The bot needs **Message Content Intent** and **Server Members Intent** enabled
> in the Discord Developer Portal.  
> Assign a role with *Timeout Members* + *Manage Messages* for full control.

---

## 〽️ Design notes

* **Real‑time** — no polling delays; uses WebSocket events.
* **User privacy** — messages are not stored; only offence counts per user ID.
* **Graceful** — warns before muting, feels fair.
* **Extensible** — swap moderation model, add custom rules, or integrate
  perspective API.

---

## 🛣️ Next steps if I had more time

* **Dashboard** showing violations over time (Grafana + Prometheus).
* **Customisable rules** via slash commands (e.g., set threshold per channel).
* **Multilingual support** with Whisper for voice channels.
* **Appeal system** allowing users to request review of false positives.

---

## 🪪 License

MIT
