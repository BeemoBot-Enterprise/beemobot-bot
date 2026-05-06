# BeemoBot — Discord bot + Match Worker

Python Discord bot for the BeemoBot ecosystem. Two processes share this codebase:
- **Bot** : slash commands + DM dispatcher
- **Worker** : background poller of Riot match histories

Companion projects: [`beemobot-api`](../beemobot-api) · [`beemobot-webapp`](../beemobot-webapp).

## Stack

- Python 3.11+
- discord.py 2.4 (slash commands + UI Views)
- aiohttp (async HTTP to API)
- riotwatcher (Riot API client for sync calls)
- psycopg2-binary (worker DB access)

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # fill values
```

## Env

| Var | Purpose |
|---|---|
| `BOT_TOKEN_TEST` / `BOT_TOKEN_PROD` | Discord bot token (TEST in dev, PROD with `ENV=production`) |
| `RIOT_API_KEY` | Riot API key (same as in beemobot-api/.env) |
| `BEEMO_API_BASE_URL` | API base URL (default `https://api.beemobot.fr`) |
| `WEBAPP_URL` | Webapp URL (used by `/link` command, default `http://localhost:3000`) |
| `DB_*` | Postgres (worker reads from same DB as API) |
| `WORKER_INTERVAL_S` | Poll cadence in seconds (default 300) |
| `DM_INTERVAL_S` | DM consumer poll cadence (default 30) |

## Run

Two terminals:

```bash
# Bot (slash commands + DM consumer)
python main.py

# Worker (Riot poller)
python -m worker.main
```

## Slash commands

- `/link` — start Discord ↔ Riot linking flow
- `/me Riot-Tag` — view your rep + honey
- `/judge Riot-Tag` — reactive: list eligible matches, give rep via buttons
- `/lastgame name tag region` — Riot stats
- `/runes role` — Teemo runes for a role
- `/help_orion` — info embed
- `/setup` — admin per-server config

## Architecture

- `Discord/Commands/` — one file per slash command + `rep_buttons.py` (reusable Discord UI View)
- `Discord/Commands/api_beemo.py` — async client for the BeemoBot API
- `Riot/` — riotwatcher helpers
- `worker/` — match poller + DM dispatcher (separate process)
- `config.py` — env vars + region maps
- `Verification/` / `Logs/` — startup checks + logging

## See also

- [`../CLAUDE.md`](../CLAUDE.md) — ecosystem map
- [`../beemobot-api/docs/superpowers/specs/2026-05-06-beemobot-rep-system-design.md`](../beemobot-api/docs/superpowers/specs/2026-05-06-beemobot-rep-system-design.md) — full product spec

## License

Copyright (c) 2024-2026 BeemoBot Enterprise. All rights reserved.
