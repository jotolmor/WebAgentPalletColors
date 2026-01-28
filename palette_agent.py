#!/usr/bin/env python3
"""LLM palette agent helper for web designers."""
from __future__ import annotations

import argparse
import json

from palette_core import generate_palette


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Genera paletas de color para diseñadores web a partir de un sentimiento/idea.",
    )
    parser.add_argument("sentiment", help="Sentimiento principal (ej. calma, energia, confianza).")
    parser.add_argument("idea", help="Idea o concepto de apoyo para la paleta.")
    parser.add_argument("--count", type=int, default=5, help="Número de colores a generar.")
    parser.add_argument("--seed", type=int, default=None, help="Semilla opcional para reproducibilidad.")
    parser.add_argument(
        "--style",
        type=str,
        default=None,
        help="Estilo visual (minimalista, brutalista, retro, futurista).",
    )
    parser.add_argument(
        "--brand",
        type=str,
        default=None,
        help="Pista de marca o logo para mantener coherencia.",
    )
    parser.add_argument(
        "--ab",
        type=str,
        nargs=2,
        metavar=("ESTILO_A", "ESTILO_B"),
        help="Genera un comparador A/B con dos estilos.",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.ab:
        style_a, style_b = args.ab
        result = {
            "comparison": {
                "a": generate_palette(
                    args.sentiment,
                    args.idea,
                    args.count,
                    args.seed,
                    style_a,
                    args.brand,
                ),
                "b": generate_palette(
                    args.sentiment,
                    args.idea,
                    args.count,
                    args.seed,
                    style_b,
                    args.brand,
                ),
            }
        }
    else:
        result = generate_palette(
            args.sentiment,
            args.idea,
            args.count,
            args.seed,
            args.style,
            args.brand,
        )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
