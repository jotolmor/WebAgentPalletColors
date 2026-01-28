#!/usr/bin/env python3
"""Core palette generation utilities for the web palette agent."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Tuple
import random


@dataclass(frozen=True)
class PaletteProfile:
    name: str
    base_hues: List[int]
    saturation_range: Tuple[int, int]
    lightness_range: Tuple[int, int]
    notes: str


PROFILES: Dict[str, PaletteProfile] = {
    "alegria": PaletteProfile(
        name="alegria",
        base_hues=[45, 55, 35, 60, 25],
        saturation_range=(65, 90),
        lightness_range=(55, 70),
        notes="Amarillos cálidos para sensaciones alegres y vitales.",
    ),
    "amor": PaletteProfile(
        name="amor",
        base_hues=[330, 345, 350, 320, 10],
        saturation_range=(50, 80),
        lightness_range=(50, 65),
        notes="Rosas y rojos suaves para afecto y cercanía.",
    ),
    "gratitud": PaletteProfile(
        name="gratitud",
        base_hues=[45, 80, 30, 20, 60],
        saturation_range=(40, 65),
        lightness_range=(55, 75),
        notes="Tonos cálidos y dorados para reconocimiento y calidez.",
    ),
    "interes": PaletteProfile(
        name="interes",
        base_hues=[200, 260, 300, 220, 180],
        saturation_range=(45, 70),
        lightness_range=(45, 65),
        notes="Azules y púrpuras para curiosidad y exploración.",
    ),
    "orgullo": PaletteProfile(
        name="orgullo",
        base_hues=[280, 260, 240, 300, 220],
        saturation_range=(40, 70),
        lightness_range=(40, 60),
        notes="Púrpuras profundos para admiración y respeto.",
    ),
    "esperanza": PaletteProfile(
        name="esperanza",
        base_hues=[140, 160, 120, 170, 100],
        saturation_range=(35, 60),
        lightness_range=(55, 75),
        notes="Verdes frescos para optimismo y renovación.",
    ),
    "inspiracion": PaletteProfile(
        name="inspiracion",
        base_hues=[280, 200, 320, 260, 340],
        saturation_range=(55, 80),
        lightness_range=(50, 65),
        notes="Violetas creativos para motivación e ideas.",
    ),
    "calma": PaletteProfile(
        name="calma",
        base_hues=[190, 200, 210, 220, 180],
        saturation_range=(18, 40),
        lightness_range=(70, 92),
        notes="Paleta suave, ideal para interfaces relajantes.",
    ),
    "energia": PaletteProfile(
        name="energia",
        base_hues=[15, 25, 40, 5, 330],
        saturation_range=(65, 90),
        lightness_range=(45, 60),
        notes="Colores intensos y vibrantes para transmitir dinamismo.",
    ),
    "confianza": PaletteProfile(
        name="confianza",
        base_hues=[205, 215, 225, 240, 200],
        saturation_range=(45, 70),
        lightness_range=(35, 55),
        notes="Azules sólidos con contraste moderado para credibilidad.",
    ),
    "creatividad": PaletteProfile(
        name="creatividad",
        base_hues=[280, 300, 320, 260, 340],
        saturation_range=(55, 85),
        lightness_range=(50, 65),
        notes="Magentas y púrpuras para ideas originales.",
    ),
    "naturaleza": PaletteProfile(
        name="naturaleza",
        base_hues=[95, 110, 120, 80, 140],
        saturation_range=(40, 65),
        lightness_range=(35, 65),
        notes="Verdes orgánicos con equilibrio de brillo.",
    ),
    "lujo": PaletteProfile(
        name="lujo",
        base_hues=[40, 50, 25, 330, 0],
        saturation_range=(25, 55),
        lightness_range=(25, 45),
        notes="Dorado y borgoña para sensaciones premium.",
    ),
    "miedo": PaletteProfile(
        name="miedo",
        base_hues=[210, 220, 200, 230, 180],
        saturation_range=(20, 45),
        lightness_range=(20, 40),
        notes="Azules fríos y oscuros para tensión y alarma.",
    ),
    "tristeza": PaletteProfile(
        name="tristeza",
        base_hues=[210, 220, 230, 200, 240],
        saturation_range=(20, 45),
        lightness_range=(25, 45),
        notes="Azules apagados para melancolía y recogimiento.",
    ),
    "ira": PaletteProfile(
        name="ira",
        base_hues=[0, 10, 350, 20, 340],
        saturation_range=(70, 90),
        lightness_range=(35, 55),
        notes="Rojos intensos para fuerza y tensión.",
    ),
    "asco": PaletteProfile(
        name="asco",
        base_hues=[90, 110, 70, 120, 60],
        saturation_range=(35, 60),
        lightness_range=(30, 50),
        notes="Verdes ácidos para rechazo y aversión.",
    ),
    "verguenza": PaletteProfile(
        name="verguenza",
        base_hues=[10, 350, 30, 0, 20],
        saturation_range=(30, 55),
        lightness_range=(30, 45),
        notes="Rojos apagados para incomodidad y culpa.",
    ),
    "celos": PaletteProfile(
        name="celos",
        base_hues=[95, 110, 130, 80, 140],
        saturation_range=(40, 65),
        lightness_range=(30, 50),
        notes="Verdes oscuros para recelo y posesividad.",
    ),
    "aburrimiento": PaletteProfile(
        name="aburrimiento",
        base_hues=[210, 0, 60, 180, 240],
        saturation_range=(5, 25),
        lightness_range=(60, 80),
        notes="Grises y bajos contrastes para apatía.",
    ),
}

STYLE_MODIFIERS: Dict[str, Dict[str, Tuple[int, int]]] = {
    "minimalista": {"saturation_range": (10, 30), "lightness_range": (75, 95)},
    "brutalista": {"saturation_range": (70, 95), "lightness_range": (45, 60)},
    "retro": {"saturation_range": (45, 70), "lightness_range": (50, 70)},
    "futurista": {"saturation_range": (55, 85), "lightness_range": (40, 60)},
}

SENTIMENT_SYNONYMS: Dict[str, str] = {
    "alegría": "alegria",
    "bienestar": "alegria",
    "diversion": "alegria",
    "diversión": "alegria",
    "gozo": "alegria",
    "felicidad": "alegria",
    "placer": "alegria",
    "amor": "amor",
    "afecto": "amor",
    "cariño": "amor",
    "ternura": "amor",
    "conexion": "amor",
    "conexión": "amor",
    "devocion": "amor",
    "devoción": "amor",
    "gratitud": "gratitud",
    "agradecimiento": "gratitud",
    "reconocimiento": "gratitud",
    "serenidad": "calma",
    "tranquilidad": "calma",
    "relax": "calma",
    "paz interior": "calma",
    "sosiego": "calma",
    "interes": "interes",
    "interés": "interes",
    "curiosidad": "interes",
    "fascinacion": "interes",
    "fascinación": "interes",
    "intriga": "interes",
    "orgullo": "orgullo",
    "admiracion": "orgullo",
    "admiración": "orgullo",
    "esperanza": "esperanza",
    "ilusion": "esperanza",
    "ilusión": "esperanza",
    "optimismo": "esperanza",
    "inspiracion": "inspiracion",
    "inspiración": "inspiracion",
    "motivacion": "inspiracion",
    "motivación": "inspiracion",
    "energía": "energia",
    "vitalidad": "energia",
    "poder": "confianza",
    "seguridad": "confianza",
    "miedo": "miedo",
    "ansiedad": "miedo",
    "temor": "miedo",
    "panico": "miedo",
    "pánico": "miedo",
    "alarma": "miedo",
    "susto": "miedo",
    "tristeza": "tristeza",
    "pena": "tristeza",
    "desanimo": "tristeza",
    "desánimo": "tristeza",
    "soledad": "tristeza",
    "congoja": "tristeza",
    "desesperacion": "tristeza",
    "desesperación": "tristeza",
    "ira": "ira",
    "enojo": "ira",
    "rabia": "ira",
    "frustracion": "ira",
    "frustración": "ira",
    "resentimiento": "ira",
    "furia": "ira",
    "irritacion": "ira",
    "irritación": "ira",
    "asco": "asco",
    "repugnancia": "asco",
    "disgusto": "asco",
    "aversion": "asco",
    "aversión": "asco",
    "verguenza": "verguenza",
    "vergüenza": "verguenza",
    "culpa": "verguenza",
    "bochorno": "verguenza",
    "remordimiento": "verguenza",
    "autocritica": "verguenza",
    "auto-crítica": "verguenza",
    "celos": "celos",
    "envidia": "celos",
    "recelo": "celos",
    "aburrimiento": "aburrimiento",
    "indiferencia": "aburrimiento",
    "apatia": "aburrimiento",
    "apatía": "aburrimiento",
    "desinteres": "aburrimiento",
    "desinterés": "aburrimiento",
    "innovacion": "creatividad",
    "innovación": "creatividad",
    "organico": "naturaleza",
    "orgánico": "naturaleza",
    "premium": "lujo",
    "elegancia": "lujo",
}


def clamp(value: float, minimum: float, maximum: float) -> float:
    return max(minimum, min(value, maximum))


def hsl_to_rgb(h: float, s: float, l: float) -> Tuple[int, int, int]:
    h = h % 360
    s = clamp(s, 0, 100) / 100
    l = clamp(l, 0, 100) / 100

    c = (1 - abs(2 * l - 1)) * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = l - c / 2

    if 0 <= h < 60:
        r1, g1, b1 = c, x, 0
    elif 60 <= h < 120:
        r1, g1, b1 = x, c, 0
    elif 120 <= h < 180:
        r1, g1, b1 = 0, c, x
    elif 180 <= h < 240:
        r1, g1, b1 = 0, x, c
    elif 240 <= h < 300:
        r1, g1, b1 = x, 0, c
    else:
        r1, g1, b1 = c, 0, x

    r = int(round((r1 + m) * 255))
    g = int(round((g1 + m) * 255))
    b = int(round((b1 + m) * 255))
    return r, g, b


def rgb_to_hsl(r: int, g: int, b: int) -> Tuple[int, int, int]:
    r_n = clamp(r, 0, 255) / 255
    g_n = clamp(g, 0, 255) / 255
    b_n = clamp(b, 0, 255) / 255
    max_c = max(r_n, g_n, b_n)
    min_c = min(r_n, g_n, b_n)
    delta = max_c - min_c

    l = (max_c + min_c) / 2

    if delta == 0:
        h = 0
        s = 0
    else:
        s = delta / (1 - abs(2 * l - 1)) if l else 0
        if max_c == r_n:
            h = ((g_n - b_n) / delta) % 6
        elif max_c == g_n:
            h = (b_n - r_n) / delta + 2
        else:
            h = (r_n - g_n) / delta + 4
        h *= 60

    return int(round(h)), int(round(s * 100)), int(round(l * 100))


def format_color(r: int, g: int, b: int, alpha: float) -> Dict[str, str]:
    hex_value = f"#{r:02X}{g:02X}{b:02X}"
    h, s, l = rgb_to_hsl(r, g, b)
    return {
        "rgb": f"rgb({r}, {g}, {b})",
        "rgba": f"rgba({r}, {g}, {b}, {alpha:.2f})",
        "hex": hex_value,
        "hsl": f"hsl({h}, {s}%, {l}%)",
        "hsla": f"hsla({h}, {s}%, {l}%, {alpha:.2f})",
    }


def relative_luminance(r: int, g: int, b: int) -> float:
    def channel(value: float) -> float:
        value = clamp(value, 0, 255) / 255
        return value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4

    r_l = channel(r)
    g_l = channel(g)
    b_l = channel(b)
    return 0.2126 * r_l + 0.7152 * g_l + 0.0722 * b_l


def contrast_ratio(rgb1: Tuple[int, int, int], rgb2: Tuple[int, int, int]) -> float:
    l1 = relative_luminance(*rgb1)
    l2 = relative_luminance(*rgb2)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def best_text_color(rgb: Tuple[int, int, int]) -> str:
    luminance = relative_luminance(*rgb)
    return "#0f172a" if luminance > 0.6 else "#f8fafc"


def harmony_suggestions(base_hue: int) -> List[Dict[str, object]]:
    return [
        {"name": "Complementaria", "hues": [base_hue, (base_hue + 180) % 360]},
        {"name": "Análoga", "hues": [(base_hue - 30) % 360, base_hue, (base_hue + 30) % 360]},
        {"name": "Triádica", "hues": [base_hue, (base_hue + 120) % 360, (base_hue + 240) % 360]},
    ]


def generate_palette(
    sentiment: str,
    idea: str,
    count: int,
    seed: int | None,
    style: str | None,
    brand_hint: str | None,
) -> Dict[str, object]:
    normalized = (sentiment or "").strip().lower()
    normalized = SENTIMENT_SYNONYMS.get(normalized, normalized)
    profile = PROFILES.get(normalized, PROFILES["confianza"])

    style_key = (style or "").strip().lower()
    style_modifier = STYLE_MODIFIERS.get(style_key)
    if style_modifier:
        profile = PaletteProfile(
            name=f"{profile.name}-{style_key}",
            base_hues=profile.base_hues,
            saturation_range=style_modifier["saturation_range"],
            lightness_range=style_modifier["lightness_range"],
            notes=f"{profile.notes} Estilo aplicado: {style_key}.",
        )

    rng = random.Random(seed)
    colors = []
    rgb_values: List[Tuple[int, int, int]] = []
    for index in range(count):
        hue_base = profile.base_hues[index % len(profile.base_hues)]
        hue_variation = rng.randint(-8, 8)
        hue = (hue_base + hue_variation) % 360
        saturation = rng.randint(*profile.saturation_range)
        lightness = rng.randint(*profile.lightness_range)
        r, g, b = hsl_to_rgb(hue, saturation, lightness)
        alpha = rng.uniform(0.75, 0.95)
        rgb_values.append((r, g, b))
        colors.append(
            {
                "name": f"Color {index + 1}",
                "hue": hue,
                "saturation": saturation,
                "lightness": lightness,
                "formats": format_color(r, g, b, alpha),
                "text": best_text_color((r, g, b)),
            }
        )

    contrast_pairs = []
    for i in range(len(rgb_values)):
        for j in range(i + 1, len(rgb_values)):
            ratio = contrast_ratio(rgb_values[i], rgb_values[j])
            contrast_pairs.append(ratio)
    min_contrast = min(contrast_pairs) if contrast_pairs else 0.0
    contrast_note = (
        "Contraste bajo detectado, considera ajustar luminosidad o saturación."
        if min_contrast < 4.5
        else "Contraste general adecuado para texto estándar."
    )

    suggestions = [
        "Ajusta el contraste según WCAG para textos y fondos.",
        "Define un color dominante, dos secundarios y dos de acento.",
        "Verifica la paleta en modo oscuro si la interfaz lo requiere.",
        "Testea accesibilidad con simuladores de daltonismo.",
        "Aplica reglas de armonía (análoga, complementaria, triádica) si buscas consistencia.",
        "Ofrece una variante de alto contraste para lectores con baja visión.",
        "Guarda presets por marca para mantener coherencia entre campañas.",
    ]
    if brand_hint:
        suggestions.append(
            "Considera extraer un color principal del logo para mantener coherencia de marca."
        )

    base_hue = colors[0]["hue"] if colors else 0
    return {
        "sentiment": sentiment,
        "idea": idea,
        "profile": profile.name,
        "notes": profile.notes,
        "palette": colors,
        "contrast": {
            "min_ratio": round(min_contrast, 2),
            "note": contrast_note,
        },
        "harmony": harmony_suggestions(base_hue),
        "brand_hint": brand_hint,
        "style": style_key or None,
        "ai_notes": [
            "Variaciones generadas con heurísticas de color para simular enfoque creativo.",
            "Aplica reglas de concordancia para coherencia visual.",
        ],
        "suggestions": suggestions,
    }


def generate_ai_variations(
    sentiment: str,
    idea: str,
    count: int,
    seed: int | None,
) -> List[Dict[str, object]]:
    styles = ["minimalista", "retro", "futurista"]
    variations = []
    for index, style in enumerate(styles):
        variations.append(
            generate_palette(
                sentiment,
                idea,
                count,
                None if seed is None else seed + index + 1,
                style,
                None,
            )
        )
    return variations


def build_design_tokens(palette: List[Dict[str, Any]]) -> Dict[str, str]:
    tokens: Dict[str, str] = {}
    for index, color in enumerate(palette, start=1):
        formats = color.get("formats", {})
        tokens[f"palette-{index}"] = formats.get("hex", "") if isinstance(formats, dict) else ""
    return tokens


def export_tokens_to_css(palette: List[Dict[str, object]]) -> str:
    tokens = build_design_tokens(palette)
    lines = [":root {"]
    for key, value in tokens.items():
        lines.append(f"  --{key}: {value};")
    lines.append("}")
    return "\n".join(lines)


def export_tokens_to_tailwind(palette: List[Dict[str, object]]) -> Dict[str, object]:
    tokens = build_design_tokens(palette)
    return {
        "theme": {
            "extend": {
                "colors": tokens,
            }
        }
    }


def export_tokens_to_figma(palette: List[Dict[str, object]]) -> Dict[str, object]:
    tokens = build_design_tokens(palette)
    return {
        "colors": {
            name: {"value": value, "type": "color"} for name, value in tokens.items()
        }
    }
