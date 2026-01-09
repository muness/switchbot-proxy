#!/usr/bin/env python3
"""Switchbot API proxy that handles HMAC signing."""

import asyncio
import hashlib
import hmac
import base64
import time
import uuid
import os

import aiohttp
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Switchbot Proxy")

TOKEN = os.environ.get("SWITCHBOT_TOKEN")
SECRET = os.environ.get("SWITCHBOT_SECRET")
API_BASE = "https://api.switch-bot.com/v1.1"


def make_headers() -> dict:
    """Generate signed headers for Switchbot API."""
    t = str(int(time.time() * 1000))
    nonce = str(uuid.uuid4())
    string_to_sign = f"{TOKEN}{t}{nonce}"
    sign = base64.b64encode(
        hmac.new(SECRET.encode(), string_to_sign.encode(), hashlib.sha256).digest()
    ).decode()
    return {
        "Authorization": TOKEN,
        "sign": sign,
        "t": t,
        "nonce": nonce,
        "Content-Type": "application/json",
    }


class CommandRequest(BaseModel):
    command: str = "turnOn"
    parameter: str = "default"
    commandType: str = "command"


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/devices")
async def list_devices():
    """List all devices."""
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_BASE}/devices", headers=make_headers()) as resp:
            return await resp.json()


@app.post("/devices/{device_id}/turnOn")
async def turn_on(device_id: str):
    """Send turnOn command (triggers customize mode sequence)."""
    return await send_command(device_id, "turnOn")


@app.post("/devices/{device_id}/turnOff")
async def turn_off(device_id: str):
    """Send turnOff command."""
    return await send_command(device_id, "turnOff")


@app.post("/devices/{device_id}/press")
async def press(device_id: str):
    """Send press command (no-op in customize mode)."""
    return await send_command(device_id, "press")


@app.post("/devices/{device_id}/command")
async def custom_command(device_id: str, req: CommandRequest):
    """Send arbitrary command."""
    return await send_command(device_id, req.command, req.parameter, req.commandType)


async def send_command(
    device_id: str,
    command: str,
    parameter: str = "default",
    command_type: str = "command",
) -> dict:
    """Send command to device."""
    payload = {
        "command": command,
        "parameter": parameter,
        "commandType": command_type,
    }
    async with aiohttp.ClientSession() as session:
        url = f"{API_BASE}/devices/{device_id}/commands"
        async with session.post(url, headers=make_headers(), json=payload) as resp:
            result = await resp.json()
            if result.get("statusCode") != 100:
                raise HTTPException(status_code=400, detail=result)
            return result


@app.get("/devices/{device_id}/status")
async def get_status(device_id: str):
    """Get device status."""
    async with aiohttp.ClientSession() as session:
        url = f"{API_BASE}/devices/{device_id}/status"
        async with session.get(url, headers=make_headers()) as resp:
            return await resp.json()
