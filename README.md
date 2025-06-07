Below is a complete **`README.md`** you can drop straight into the root of the **`discord_guardian_bot`** repository.
Copy-paste (or save) it as-is; every bracketed link and badge is ready to work once you add the demo assets.

````markdown
# Discord Guardian Bot 🛡️  
*AI-powered, real-time toxicity watchdog for Discord servers*

[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-yellow.svg)

---

## ✨ Why?

Small and mid-sized communities rarely have 24 × 7 human moderation.  
A single hateful or threatening message can ruin the vibe before staff wake up.  
**Discord Guardian Bot** jumps in instantly: flags toxic content, warns the author, and auto-mutes repeat offenders—while logging everything for review.

---

## 🚀 Features

| ✔ | Capability | Notes |
|---|------------|-------|
| ⚡ **Real-time scanning** | <1 s latency via Discord Gateway |
| 🤖 **OpenAI moderation** | Uses `text-moderation-latest` for hate / harassment / violence detection |
| 🛑 **Gentle escalation** | 1-st & 2-nd strike: polite warning   3-rd strike: configurable timeout |
| 🗃 **Audit log embeds** | Posts rich embeds to a `#moderation-log` channel |
| 🔧 **.env-driven config** | Tokens, thresholds, guild/channel IDs, mute length, log level |
| 📜 **Verbose DEBUG mode** | See every decision & raw OpenAI response for easy debugging |
| 🐳 **Docker-ready** | One-command deploy anywhere |

---

## 🏗 Architecture

```text
Discord Gateway (WebSocket events)
            │
            ▼
   discord.py client  ⇢  OpenAI Moderation API
            │                    │
            │                    ▼
            │           JSON verdict  (hate / violence / etc.)
            ▼
 Guardian bot logic
   • warn user
   • count strikes → timeout
   • log embed → #moderation-log
   • persist strikes in violations.json
````

---

## 📦 Requirements

* **Discord** bot application with **Message Content Intent** enabled
* **OpenAI** account with API key and active billing / remaining credit
* Python 3.11+ **or** Docker (to run container)

---

## 🛠️ Setup

1. **Clone & install**

   ```bash
   git clone https://github.com/yourname/discord-guardian-bot.git
   cd discord-guardian-bot
   python -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Create a bot in the Discord Developer Portal**

   * Enable **Message Content Intent** & **Server Members Intent**.
   * Copy the bot token.

3. **Invite the bot**
   In *OAuth2 → URL Generator*, select **bot** scope and grant:
   `Read Messages`, `Send Messages`, `Embed Links`, `Manage Messages`, `Timeout Members`.
   Paste the URL, invite the bot, and (optionally) create `#moderation-log`.

4. **Fill environment variables**

   ```bash
   cp .env.example .env
   # then edit .env with your keys & IDs
   ```

   | Variable            | Description                                 |
   | ------------------- | ------------------------------------------- |
   | `DISCORD_BOT_TOKEN` | Bot token from step 2                       |
   | `OPENAI_API_KEY`    | Your OpenAI key                             |
   | `GUILD_ID`          | (Optional) server ID to restrict moderation |
   | `LOG_CHANNEL_ID`    | Channel ID for log embeds                   |
   | `WARN_THRESHOLD`    | Strikes before mute (default 2)             |
   | `MUTE_DURATION_MIN` | Timeout length (default 30 min)             |
   | `LOG_LEVEL`         | `INFO` or `DEBUG`                           |

5. **Run**

   ```bash
   python bot.py
   # or:
   docker build -t guardian-bot .
   docker run --env-file .env guardian-bot
   ```

---

## 🔎 Testing

Paste any of these strings in a channel the bot can read:

```
You're such a worthless loser—go crawl back under your rock.
Say that again and I'll smash your face in.
```

You should see:

* ⚠️ warning reply in-channel
* embed in `#moderation-log`
* user timed-out on the N-th strike

> **DEBUG mode** (`LOG_LEVEL=DEBUG`) prints raw moderation responses & every internal step.

---

## 📝 Design Choices

* **No database** – a tiny `violations.json` keeps state; perfect for hack-scale.
* **Polite UX** – always warns before punishing, wording is constructive.
* **Graceful degradation** – if OpenAI quota is exhausted, bot logs the error and skips moderation (no crashes).
* **Extensible** – swap in Perspective API or custom models by editing `moderation.py`.

---

## 🛣️ Roadmap

* Slash-command dashboard to adjust thresholds live
* Whisper integration for voice-chat toxicity detection
* Prometheus exporter → Grafana toxicity heat-map
* Adaptive mute length (longer for multiple offences over time)
* Auto-delete flagged messages after warning

---

## 📄 License

MIT – do what you want, just keep the notice.

---

## 🎥 Demo

> *2-min screen-recording walk-through link goes here (e.g., Loom or YouTube).*

---

Enjoy safer conversations! PRs and feedback welcome 💬

```

**How to use**

1. Save the block above as `README.md`.
2. Replace placeholders (`yourname`, demo link, etc.).
3. Commit & push—your repo now has a polished, self-contained read-me for reviewers.

That’s it!
```
