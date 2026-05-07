# Last updated: 2026-05-07
"""Tiny aiohttp server exposing /health alongside the Discord client.

Runs in the same event loop as discord.py so it can read live bot state
(connection, latency, user). Used by Coolify / UptimeRobot probes.
"""
import asyncio
import logging
import os
from aiohttp import web

logger = logging.getLogger(__name__)

HEALTH_PORT = int(os.getenv("HEALTH_PORT", "8080"))


def _health_payload(bot):
    is_ready = bot.is_ready()
    return {
        "status": "ok" if is_ready else "starting",
        "discord": "connected" if is_ready else "disconnected",
        "user": str(bot.user) if bot.user else None,
        "latency_ms": round(bot.latency * 1000, 2) if is_ready else None,
    }


async def run_health_server(bot):
    """Start an HTTP server and keep it alive for the lifetime of the bot."""
    app = web.Application()

    async def health(_request):
        payload = _health_payload(bot)
        status = 200 if payload["status"] == "ok" else 503
        return web.json_response(payload, status=status)

    app.router.add_get("/", health)
    app.router.add_get("/health", health)

    runner = web.AppRunner(app, access_log=None)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", HEALTH_PORT)
    await site.start()
    logger.info("Health server listening on 0.0.0.0:%s", HEALTH_PORT)

    try:
        # Keep the task alive so runner/site stay in scope
        await asyncio.Event().wait()
    finally:
        await runner.cleanup()
