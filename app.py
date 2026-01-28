#!/usr/bin/env python3
"""FastAPI web app and API for palette generation."""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from palette_core import (
    export_tokens_to_css,
    export_tokens_to_figma,
    export_tokens_to_tailwind,
    generate_ai_variations,
    generate_palette,
)

app = FastAPI(title="Web Palette Agent")
BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")
PRESETS_PATH = os.path.join(DATA_DIR, "presets.json")

app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))


class PaletteRequest(BaseModel):
    sentiment: str = ""
    idea: str = ""
    count: int = 5
    seed: Optional[int] = None
    style: Optional[str] = None
    brand: Optional[str] = None


class ExportRequest(PaletteRequest):
    format: str = "css"


def load_presets() -> List[Dict[str, Any]]:
    if not os.path.exists(PRESETS_PATH):
        return []
    with open(PRESETS_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def save_preset(entry: Dict[str, Any]) -> None:
    os.makedirs(DATA_DIR, exist_ok=True)
    presets = load_presets()
    presets.append(entry)
    with open(PRESETS_PATH, "w", encoding="utf-8") as file:
        json.dump(presets, file, ensure_ascii=False, indent=2)


def palette_payload(payload: PaletteRequest) -> Dict[str, Any]:
    return generate_palette(
        payload.sentiment,
        payload.idea,
        payload.count,
        payload.seed,
        payload.style,
        payload.brand,
    )


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/api/palette")
async def api_palette(payload: PaletteRequest) -> JSONResponse:
    palette = palette_payload(payload)
    preset_entry = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "sentiment": palette.get("sentiment"),
        "idea": palette.get("idea"),
        "style": palette.get("style"),
        "brand_hint": palette.get("brand_hint"),
        "palette": palette.get("palette"),
    }
    save_preset(preset_entry)
    return JSONResponse(palette)


@app.get("/api/presets")
async def api_presets() -> JSONResponse:
    return JSONResponse(load_presets())


@app.post("/api/export")
async def api_export(payload: ExportRequest) -> JSONResponse:
    palette = palette_payload(payload)
    fmt = payload.format.lower()
    if fmt == "css":
        return JSONResponse({"format": "css", "content": export_tokens_to_css(palette["palette"])})
    if fmt == "tailwind":
        return JSONResponse(
            {"format": "tailwind", "content": export_tokens_to_tailwind(palette["palette"])}
        )
    if fmt == "figma":
        return JSONResponse({"format": "figma", "content": export_tokens_to_figma(palette["palette"])})
    return JSONResponse({"error": "Formato no soportado."}, status_code=400)


@app.post("/api/ai-palettes")
async def api_ai_palettes(payload: PaletteRequest) -> JSONResponse:
    variations = generate_ai_variations(
        payload.sentiment,
        payload.idea,
        payload.count,
        payload.seed,
    )
    return JSONResponse({"palettes": variations})
